// +build linux

/*
Copyright 2014 The Kubernetes Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package mount

import (
	"bufio"
	"fmt"
	"hash/adler32"
	"io"
	"os"
	"os/exec"
	"strconv"
	"strings"
	"syscall"

	"github.com/golang/glog"
	utilExec "k8s.io/kubernetes/pkg/util/exec"
)

const (
	// How many times to retry for a consistent read of /proc/mounts.
	maxListTries = 3
	// Number of fields per line in /proc/mounts as per the fstab man page.
	expectedNumFieldsPerLine = 6
	// Location of the mount file to use
	procMountsPath = "/proc/mounts"
)

const (
	// 'fsck' found errors and corrected them
	fsckErrorsCorrected = 1
	// 'fsck' found errors but exited without correcting them
	fsckErrorsUncorrected = 4
)

// Mounter provides the default implementation of mount.Interface
// for the linux platform.  This implementation assumes that the
// kubelet is running in the host's root mount namespace.
type Mounter struct {
	withSystemd bool
}

// New returns a mount.Interface for the current system.
func New() Interface {
	return &Mounter{
		withSystemd: detectSystemd(),
	}
}

// Mount mounts source to target as fstype with given options. 'source' and 'fstype' must
// be an emtpy string in case it's not required, e.g. for remount, or for auto filesystem
// type, where kernel handles fs type for you. The mount 'options' is a list of options,
// currently come from mount(8), e.g. "ro", "remount", "bind", etc. If no more option is
// required, call Mount with an empty string list or nil.
func (mounter *Mounter) Mount(source string, target string, fstype string, options []string) error {
	bind, bindRemountOpts := isBind(options)

	if bind {
		err := mounter.doMount(source, target, fstype, []string{"bind"})
		if err != nil {
			return err
		}
		return mounter.doMount(source, target, fstype, bindRemountOpts)
	} else {
		return mounter.doMount(source, target, fstype, options)
	}
}

// isBind detects whether a bind mount is being requested and makes the remount options to
// use in case of bind mount, due to the fact that bind mount doesn't respect mount options.
// The list equals:
//   options - 'bind' + 'remount' (no duplicate)
func isBind(options []string) (bool, []string) {
	bindRemountOpts := []string{"remount"}
	bind := false

	if len(options) != 0 {
		for _, option := range options {
			switch option {
			case "bind":
				bind = true
				break
			case "remount":
				break
			default:
				bindRemountOpts = append(bindRemountOpts, option)
			}
		}
	}

	return bind, bindRemountOpts
}

// doMount runs the mount command.
func (mounter *Mounter) doMount(source string, target string, fstype string, options []string) error {
	glog.V(5).Infof("Mounting %s %s %s %v", source, target, fstype, options)
	mountArgs := makeMountArgs(source, target, fstype, options)
	mountCmd := "mount"

	if mounter.withSystemd {
		// Try to run mount via systemd-run --scope. This will escape the
		// service where kubelet runs and any fuse daemons will be started in a
		// specific scope. kubelet service than can be restarted without killing
		// these fuse daemons.
		//
		// Complete command line (when mounterPath is not used):
		// systemd-run --description=... --scope -- mount -t <type> <what> <where>
		//
		// Expected flow:
		// * systemd-run creates a transient scope (=~ cgroup) and executes its
		//   argument (/bin/mount) there.
		// * mount does its job, forks a fuse daemon if necessary and finishes.
		//   (systemd-run --scope finishes at this point, returning mount's exit
		//   code and stdout/stderr - thats one of --scope benefits).
		// * systemd keeps the fuse daemon running in the scope (i.e. in its own
		//   cgroup) until the fuse daemon dies (another --scope benefit).
		//   Kubelet service can be restarted and the fuse daemon survives.
		// * When the fuse daemon dies (e.g. during unmount) systemd removes the
		//   scope automatically.
		//
		// systemd-mount is not used because it's too new for older distros
		// (CentOS 7, Debian Jessie).
		mountCmd, mountArgs = addSystemdScope("systemd-run", target, "mount", mountArgs)
	} else {
		// No systemd-run on the host (or we failed to check it), assume kubelet
		// does not run as a systemd service.
		// No code here, mountCmd and mountArgs are already populated.
	}

	command := exec.Command(mountCmd, mountArgs...)
	output, err := command.CombinedOutput()
	if err != nil {
		glog.Errorf("Mount failed: %v\nMounting arguments: %s %s %s %v\nOutput: %s\n", err, source, target, fstype, options, string(output))
		return fmt.Errorf("mount failed: %v\nMounting arguments: %s %s %s %v\nOutput: %s\n",
			err, source, target, fstype, options, string(output))
	}
	return err
}

// detectSystemd returns true if OS runs with systemd as init. When not sure
// (permission errors, ...), it returns false.
// There may be different ways how to detect systemd, this one makes sure that
// systemd-runs (needed by Mount()) works.
func detectSystemd() bool {
	if _, err := exec.LookPath("systemd-run"); err != nil {
		glog.V(2).Infof("Detected OS without systemd")
		return false
	}
	// Try to run systemd-run --scope /bin/true, that should be enough
	// to make sure that systemd is really running and not just installed,
	// which happens when running in a container with a systemd-based image
	// but with different pid 1.
	cmd := exec.Command("systemd-run", "--description=Kubernetes systemd probe", "--scope", "true")
	output, err := cmd.CombinedOutput()
	if err != nil {
		glog.V(2).Infof("Cannot run systemd-run, assuming non-systemd OS")
		glog.V(4).Infof("systemd-run failed with: %v", err)
		glog.V(4).Infof("systemd-run output: %s", string(output))
		return false
	}
	glog.V(2).Infof("Detected OS with systemd")
	return true
}

// makeMountArgs makes the arguments to the mount(8) command.
func makeMountArgs(source, target, fstype string, options []string) []string {
	// Build mount command as follows:
	//   mount [-t $fstype] [-o $options] [$source] $target
	mountArgs := []string{}
	if len(fstype) > 0 {
		mountArgs = append(mountArgs, "-t", fstype)
	}
	if len(options) > 0 {
		mountArgs = append(mountArgs, "-o", strings.Join(options, ","))
	}
	if len(source) > 0 {
		mountArgs = append(mountArgs, source)
	}
	mountArgs = append(mountArgs, target)

	return mountArgs
}

// addSystemdScope adds "system-run --scope" to given command line
func addSystemdScope(systemdRunPath, mountName, command string, args []string) (string, []string) {
	descriptionArg := fmt.Sprintf("--description=Kubernetes transient mount for %s", mountName)
	systemdRunArgs := []string{descriptionArg, "--scope", "--", command}
	return systemdRunPath, append(systemdRunArgs, args...)
}

// Unmount unmounts the target.
func (mounter *Mounter) Unmount(target string) error {
	glog.V(5).Infof("Unmounting %s", target)
	command := exec.Command("umount", target)
	output, err := command.CombinedOutput()
	if err != nil {
		return fmt.Errorf("Unmount failed: %v\nUnmounting arguments: %s\nOutput: %s\n", err, target, string(output))
	}
	return nil
}

// List returns a list of all mounted filesystems.
func (*Mounter) List() ([]MountPoint, error) {
	return listProcMounts(procMountsPath)
}

// IsLikelyNotMountPoint determines if a directory is not a mountpoint.
// It is fast but not necessarily ALWAYS correct. If the path is in fact
// a bind mount from one part of a mount to another it will not be detected.
// mkdir /tmp/a /tmp/b; mount --bin /tmp/a /tmp/b; IsLikelyNotMountPoint("/tmp/b")
// will return true. When in fact /tmp/b is a mount point. If this situation
// if of interest to you, don't use this function...
func (mounter *Mounter) IsLikelyNotMountPoint(file string) (bool, error) {
	stat, err := os.Stat(file)
	if err != nil {
		return true, err
	}
	rootStat, err := os.Lstat(file + "/..")
	if err != nil {
		return true, err
	}
	// If the directory has a different device as parent, then it is a mountpoint.
	if stat.Sys().(*syscall.Stat_t).Dev != rootStat.Sys().(*syscall.Stat_t).Dev {
		return false, nil
	}

	return true, nil
}

// DeviceOpened checks if block device in use by calling Open with O_EXCL flag.
// Returns true if open returns errno EBUSY, and false if errno is nil.
// Returns an error if errno is any error other than EBUSY.
// Returns with error if pathname is not a device.
func (mounter *Mounter) DeviceOpened(pathname string) (bool, error) {
	return exclusiveOpenFailsOnDevice(pathname)
}

// PathIsDevice uses FileInfo returned from os.Stat to check if path refers
// to a device.
func (mounter *Mounter) PathIsDevice(pathname string) (bool, error) {
	return pathIsDevice(pathname)
}

func exclusiveOpenFailsOnDevice(pathname string) (bool, error) {
	if isDevice, err := pathIsDevice(pathname); !isDevice {
		return false, fmt.Errorf(
			"PathIsDevice failed for path %q: %v",
			pathname,
			err)
	}
	fd, errno := syscall.Open(pathname, syscall.O_RDONLY|syscall.O_EXCL, 0)
	// If the device is in use, open will return an invalid fd.
	// When this happens, it is expected that Close will fail and throw an error.
	defer syscall.Close(fd)
	if errno == nil {
		// device not in use
		return false, nil
	} else if errno == syscall.EBUSY {
		// device is in use
		return true, nil
	}
	// error during call to Open
	return false, errno
}

func pathIsDevice(pathname string) (bool, error) {
	finfo, err := os.Stat(pathname)
	// err in call to os.Stat
	if err != nil {
		return false, err
	}
	// path refers to a device
	if finfo.Mode()&os.ModeDevice != 0 {
		return true, nil
	}
	// path does not refer to device
	return false, nil
}

//GetDeviceNameFromMount: given a mount point, find the device name from its global mount point
func (mounter *Mounter) GetDeviceNameFromMount(mountPath, pluginDir string) (string, error) {
	return getDeviceNameFromMount(mounter, mountPath, pluginDir)
}

func listProcMounts(mountFilePath string) ([]MountPoint, error) {
	hash1, err := readProcMounts(mountFilePath, nil)
	if err != nil {
		return nil, err
	}

	for i := 0; i < maxListTries; i++ {
		mps := []MountPoint{}
		hash2, err := readProcMounts(mountFilePath, &mps)
		if err != nil {
			return nil, err
		}
		if hash1 == hash2 {
			// Success
			return mps, nil
		}
		hash1 = hash2
	}
	return nil, fmt.Errorf("failed to get a consistent snapshot of %v after %d tries", mountFilePath, maxListTries)
}

// readProcMounts reads the given mountFilePath (normally /proc/mounts) and produces a hash
// of the contents.  If the out argument is not nil, this fills it with MountPoint structs.
func readProcMounts(mountFilePath string, out *[]MountPoint) (uint32, error) {
	file, err := os.Open(mountFilePath)
	if err != nil {
		return 0, err
	}
	defer file.Close()
	return readProcMountsFrom(file, out)
}

func readProcMountsFrom(file io.Reader, out *[]MountPoint) (uint32, error) {
	hash := adler32.New()
	scanner := bufio.NewReader(file)
	for {
		line, err := scanner.ReadString('\n')
		if err == io.EOF {
			break
		}
		fields := strings.Fields(line)
		if len(fields) != expectedNumFieldsPerLine {
			return 0, fmt.Errorf("wrong number of fields (expected %d, got %d): %s", expectedNumFieldsPerLine, len(fields), line)
		}

		fmt.Fprintf(hash, "%s", line)

		if out != nil {
			mp := MountPoint{
				Device: fields[0],
				Path:   fields[1],
				Type:   fields[2],
				Opts:   strings.Split(fields[3], ","),
			}

			freq, err := strconv.Atoi(fields[4])
			if err != nil {
				return 0, err
			}
			mp.Freq = freq

			pass, err := strconv.Atoi(fields[5])
			if err != nil {
				return 0, err
			}
			mp.Pass = pass

			*out = append(*out, mp)
		}
	}
	return hash.Sum32(), nil
}

// formatAndMount uses unix utils to format and mount the given disk
func (mounter *SafeFormatAndMount) formatAndMount(source string, target string, fstype string, options []string) error {
	options = append(options, "defaults")

	// Run fsck on the disk to fix repairable issues
	glog.V(4).Infof("Checking for issues with fsck on disk: %s", source)
	args := []string{"-a", source}
	cmd := mounter.Runner.Command("fsck", args...)
	out, err := cmd.CombinedOutput()
	if err != nil {
		ee, isExitError := err.(utilExec.ExitError)
		switch {
		case err == utilExec.ErrExecutableNotFound:
			glog.Warningf("'fsck' not found on system; continuing mount without running 'fsck'.")
		case isExitError && ee.ExitStatus() == fsckErrorsCorrected:
			glog.Infof("Device %s has errors which were corrected by fsck.", source)
		case isExitError && ee.ExitStatus() == fsckErrorsUncorrected:
			return fmt.Errorf("'fsck' found errors on device %s but could not correct them: %s.", source, string(out))
		case isExitError && ee.ExitStatus() > fsckErrorsUncorrected:
			glog.Infof("`fsck` error %s", string(out))
		}
	}

	// Try to mount the disk
	glog.V(4).Infof("Attempting to mount disk: %s %s %s", fstype, source, target)
	err = mounter.Interface.Mount(source, target, fstype, options)
	if err != nil {
		// It is possible that this disk is not formatted. Double check using diskLooksUnformatted
		notFormatted, err := mounter.diskLooksUnformatted(source)
		if err == nil && notFormatted {
			args = []string{source}
			// Disk is unformatted so format it.
			// Use 'ext4' as the default
			if len(fstype) == 0 {
				fstype = "ext4"
			}
			if fstype == "ext4" || fstype == "ext3" {
				args = []string{"-E", "lazy_itable_init=0,lazy_journal_init=0", "-F", source}
			}
			glog.Infof("Disk %q appears to be unformatted, attempting to format as type: %q with options: %v", source, fstype, args)
			cmd := mounter.Runner.Command("mkfs."+fstype, args...)
			_, err := cmd.CombinedOutput()
			if err == nil {
				// the disk has been formatted successfully try to mount it again.
				glog.Infof("Disk successfully formatted (mkfs): %s - %s %s", fstype, source, target)
				return mounter.Interface.Mount(source, target, fstype, options)
			}
			glog.Errorf("format of disk %q failed: type:(%q) target:(%q) options:(%q)error:(%v)", source, fstype, target, options, err)
			return err
		}
	}
	return err
}

// diskLooksUnformatted uses 'lsblk' to see if the given disk is unformated
func (mounter *SafeFormatAndMount) diskLooksUnformatted(disk string) (bool, error) {
	args := []string{"-nd", "-o", "FSTYPE", disk}
	cmd := mounter.Runner.Command("lsblk", args...)
	glog.V(4).Infof("Attempting to determine if disk %q is formatted using lsblk with args: (%v)", disk, args)
	dataOut, err := cmd.CombinedOutput()
	output := strings.TrimSpace(string(dataOut))

	// TODO (#13212): check if this disk has partitions and return false, and
	// an error if so.

	if err != nil {
		glog.Errorf("Could not determine if disk %q is formatted (%v)", disk, err)
		return false, err
	}

	return output == "", nil
}
