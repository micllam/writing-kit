package writingkit

import (
	"bytes"
	"errors"
	"flag"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"testing"
)

var update = flag.Bool("update", false, "write the alerts of each rule to its file in testdata/")

// The Vale command of every rule test. The hidden flags sort the alerts by file
// and make the paths relative to the fixture folder.
var valeArgs = []string{"--output=line", "--sort", "--normalize", "--relative",
	"--no-global", "--no-exit", "."}

// Each rule of styles/Micllam has a folder in fixtures/ whose .vale.ini enables
// that rule alone, and a file in testdata/ with the alerts of the folder.
func TestRules(t *testing.T) {
	vale, err := exec.LookPath("vale")
	if err != nil {
		t.Fatal(err)
	}
	rules, err := filepath.Glob(filepath.Join("styles", "Micllam", "*.yml"))
	if err != nil || len(rules) == 0 {
		t.Fatalf("no rule in styles/Micllam: %v", err)
	}

	for _, rule := range rules {
		name := strings.TrimSuffix(filepath.Base(rule), ".yml")
		t.Run(name, func(t *testing.T) {
			fixture := filepath.Join("fixtures", name)
			if _, err := os.Stat(filepath.Join(fixture, ".vale.ini")); err != nil {
				t.Fatalf("%s has no fixture: %v", name, err)
			}

			cmd := exec.Command(vale, valeArgs...)
			cmd.Dir = fixture
			got, err := cmd.Output()
			var exit *exec.ExitError
			if errors.As(err, &exit) {
				t.Fatalf("vale in %s: %v\n%s", fixture, err, exit.Stderr)
			} else if err != nil {
				t.Fatalf("vale in %s: %v", fixture, err)
			}

			expected := filepath.Join("testdata", name+".txt")
			if *update {
				if err := os.WriteFile(expected, got, 0o644); err != nil {
					t.Fatal(err)
				}
				return
			}
			want, err := os.ReadFile(expected)
			if err != nil {
				t.Fatalf("%s has no expected alerts: %v", name, err)
			}
			if !bytes.Equal(got, want) {
				t.Errorf("alerts of %s differ from %s\nwant:\n%s\ngot:\n%s",
					fixture, expected, want, got)
			}
		})
	}
}
