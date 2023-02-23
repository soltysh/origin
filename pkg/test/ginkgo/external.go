package ginkgo

import (
	"bytes"
	"context"
	"encoding/json"
	"io"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"

	"github.com/openshift/origin/test/extended/util/annotate/generated"
)

type serializedTest struct {
	Name string
}

func externalTestsForSuite(ctx context.Context) ([]*testCase, error) {
	var tests []*testCase

	// TODO: make the binary name configurable
	testBinary := filepath.Dir(os.Args[0]) + "/k8s-tests"
	command := exec.Command(testBinary, "list")

	testList, err := runWithTimeout(ctx, command, 1*time.Minute)
	if err != nil {
		return nil, err
	}
	buf := bytes.NewBuffer(testList)
	for {
		line, err := buf.ReadString('\n')
		if err == io.EOF {
			break
		}
		if !strings.HasPrefix(line, "[{") {
			continue
		}
		serializedTests := []serializedTest{}
		err = json.Unmarshal([]byte(line), &serializedTests)
		if err != nil {
			return nil, err
		}
		for _, test := range serializedTests {
			if append, ok := generated.Annotations[test.Name]; ok {
				test.Name += append
			}
			tests = append(tests, &testCase{
				name:       test.Name,
				binaryName: testBinary,
			})
		}
	}
	return tests, nil
}
