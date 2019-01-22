package release

import (
	"testing"
)

func TestNewImageMapper(t *testing.T) {
	type args struct {
		images map[string]ImageReference
	}
	tests := []struct {
		name    string
		args    args
		input   string
		output  string
		wantErr bool
	}{
		// TODO: Add test cases.
		{name: "empty input"},
		{
			name: "empty source repository",
			args: args{
				images: map[string]ImageReference{
					"etcd": {
						TargetPullSpec: "quay.io/openshift/origin-etcd@sha256:1234",
					},
				},
			},
			wantErr: true,
		},
		{
			name: "duplicate source repositories",
			args: args{
				images: map[string]ImageReference{
					"etcd": {
						SourceRepository: "quay.io/coreos/etcd",
						TargetPullSpec:   "quay.io/openshift/origin-etcd@sha256:1234",
					},
					"etcd-2": {
						SourceRepository: "quay.io/coreos/etcd",
						TargetPullSpec:   "quay.io/openshift/origin-etcd@sha256:5678",
					},
				},
			},
			wantErr: true,
		},
		{
			name: "replace repository with tag",
			args: args{
				images: map[string]ImageReference{
					"etcd": {
						SourceRepository: "quay.io/coreos/etcd",
						TargetPullSpec:   "quay.io/openshift/origin-etcd@sha256:1234",
					},
				},
			},
			input:  "image: quay.io/coreos/etcd:latest",
			output: "image: quay.io/openshift/origin-etcd@sha256:1234",
		},
		{
			name: "replace tag with digest",
			args: args{
				images: map[string]ImageReference{
					"etcd": {
						SourceRepository: "quay.io/coreos/etcd:latest",
						TargetPullSpec:   "quay.io/openshift/origin-etcd@sha256:1234",
					},
				},
			},
			input:  "image: quay.io/coreos/etcd:latest",
			output: "image: quay.io/openshift/origin-etcd@sha256:1234",
		},
		{
			name: "replace repository with tag with trailing whitespace",
			args: args{
				images: map[string]ImageReference{
					"etcd": {
						SourceRepository: "quay.io/coreos/etcd",
						TargetPullSpec:   "quay.io/openshift/origin-etcd@sha256:1234",
					},
				},
			},
			input:  "image: quay.io/coreos/etcd:latest\n",
			output: "image: quay.io/openshift/origin-etcd@sha256:1234\n",
		},
		{
			name: "replace repository with digest",
			args: args{
				images: map[string]ImageReference{
					"etcd": {
						SourceRepository: "quay.io/coreos/etcd",
						TargetPullSpec:   "quay.io/openshift/origin-etcd@sha256:1234",
					},
				},
			},
			input:  "image: quay.io/coreos/etcd@sha256:5678",
			output: "image: quay.io/openshift/origin-etcd@sha256:1234",
		},
		{
			name: "replace with digest on a multi-line file with quotes and newlines",
			args: args{
				images: map[string]ImageReference{
					"etcd": {
						SourceRepository: "quay.io/openshift/origin-prometheus:latest",
						TargetPullSpec:   "quay.io/openshift/origin-prometheus@sha256:1234",
					},
				},
			},
			input: `
	- "-images=prometheus=quay.io/openshift/origin-prometheus:latest"
	- "-images=alertmanager=quay.io/openshift/origin-prometheus-alertmanager:latest"
`,
			output: `
	- "-images=prometheus=quay.io/openshift/origin-prometheus@sha256:1234"
	- "-images=alertmanager=quay.io/openshift/origin-prometheus-alertmanager:latest"
`,
		},
		{
			name: "replace with digest on a multi-line file with quotes and newlines",
			args: args{
				images: map[string]ImageReference{
					"etcd": {
						SourceRepository: "quay.io/openshift/origin-prometheus:latest",
						TargetPullSpec:   "quay.io/openshift/origin-prometheus@sha256:1234",
					},
				},
			},
			input: `
	- "quay.io/openshift/origin-prometheus:latest"
`,
			output: `
	- "quay.io/openshift/origin-prometheus@sha256:1234"
`,
		},
		{
			name: "replace bare repository when told to do so",
			args: args{
				images: map[string]ImageReference{
					"etcd": {
						SourceRepository: "quay.io/coreos/etcd",
						TargetPullSpec:   "quay.io/openshift/origin-etcd@sha256:1234",
					},
				},
			},
			input:  "image: quay.io/coreos/etcd",
			output: "image: quay.io/openshift/origin-etcd@sha256:1234",
		},
		{
			name: "replace bare repository with trailing whitespace when told to do so",
			args: args{
				images: map[string]ImageReference{
					"etcd": {
						SourceRepository: "quay.io/coreos/etcd",
						TargetPullSpec:   "quay.io/openshift/origin-etcd@sha256:1234",
					},
				},
			},
			input:  "image: quay.io/coreos/etcd ",
			output: "image: quay.io/openshift/origin-etcd@sha256:1234 ",
		},
		{
			name: "Ignore things that only look like images",
			args: args{
				images: map[string]ImageReference{
					"etcd": {
						SourceRepository: "quay.io/coreos/etcd",
						TargetPullSpec:   "quay.io/openshift/origin-etcd@sha256:1234",
					},
				},
			},
			input:  "example_url: https://quay.io/coreos/etcd:8443/test",
			output: "example_url: https://quay.io/coreos/etcd:8443/test",
		},
		{
			name: "replace entire file - just to verify the regex",
			args: args{
				images: map[string]ImageReference{
					"etcd": {
						SourceRepository: "quay.io/coreos/etcd",
						TargetPullSpec:   "quay.io/openshift/origin-etcd@sha256:1234",
					},
				},
			},
			input:  "quay.io/coreos/etcd:latest",
			output: "quay.io/openshift/origin-etcd@sha256:1234",
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			m, err := NewImageMapper(tt.args.images)
			if (err != nil) != tt.wantErr {
				t.Fatal(err)
			}
			if err != nil {
				return
			}
			out, err := m([]byte(tt.input))
			if (err != nil) != tt.wantErr {
				t.Fatal(err)
			}
			if err != nil {
				return
			}
			if string(out) != tt.output {
				t.Errorf("unexpected output, wanted\n%s\ngot\n%s", tt.output, string(out))
			}
		})
	}
}

func TestNewExactMapper(t *testing.T) {
	type args struct {
		mappings map[string]string
	}
	tests := []struct {
		name    string
		args    args
		input   string
		output  string
		wantErr bool
	}{
		{
			name:   "replace at end of file",
			args:   args{mappings: map[string]string{"reg/repo@sha256:01234": "reg2/repo2@sha256:01234"}},
			input:  "image: reg/repo@sha256:01234",
			output: "image: reg2/repo2@sha256:01234",
		},
		{
			name:   "replace at beginning of file",
			args:   args{mappings: map[string]string{"reg/repo@sha256:01234": "reg2/repo2@sha256:01234"}},
			input:  "reg/repo@sha256:01234",
			output: "reg2/repo2@sha256:01234",
		},
		// TODO: Add test cases.
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			m, err := NewExactMapper(tt.args.mappings)
			if (err != nil) != tt.wantErr {
				t.Fatal(err)
			}
			if err != nil {
				return
			}
			out, err := m([]byte(tt.input))
			if (err != nil) != tt.wantErr {
				t.Fatal(err)
			}
			if err != nil {
				return
			}
			if string(out) != tt.output {
				t.Errorf("unexpected output, wanted\n%s\ngot\n%s", tt.output, string(out))
			}
		})
	}
}
