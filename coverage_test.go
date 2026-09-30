package writingkit

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"testing"
)

// The files in coverage/ list the writing rules by section. Each key is true
// when the style checks the rule and false when it does not. A comment after
// the value refers to the Vale rules that check it, and every rule of
// styles/Micllam is referred to by a manifest.

var ruleRef = regexp.MustCompile(`([A-Za-z]+)\.yml`)

type tally struct {
	checked, total int
	unchecked      []string
}

func (t tally) String() string {
	return fmt.Sprintf("%3d/%-3d", t.checked, t.total)
}

func readManifest(t *testing.T, path string, referred map[string]bool) tally {
	t.Helper()
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatalf("read %s: %v", path, err)
	}

	var got tally
	for i, line := range strings.Split(string(data), "\n") {
		if idx := strings.Index(line, "#"); idx >= 0 {
			for _, m := range ruleRef.FindAllStringSubmatch(line[idx:], -1) {
				rule := filepath.Join("styles", "Micllam", m[1]+".yml")
				if _, err := os.Stat(rule); err != nil {
					t.Errorf("%s:%d: %s does not exist", path, i+1, rule)
				}
				referred[rule] = true
			}
			line = line[:idx]
		}
		line = strings.TrimSpace(line)
		if line == "" {
			continue
		}

		key, value, found := strings.Cut(line, ":")
		if !found {
			t.Errorf("%s:%d: %q is not a key and a value", path, i+1, line)
			continue
		}
		switch strings.TrimSpace(value) {
		case "true":
			got.checked++
			got.total++
		case "false":
			got.total++
			got.unchecked = append(got.unchecked, strings.TrimSpace(key))
		default:
			t.Errorf("%s:%d: the value of %s is not true or false", path, i+1,
				strings.TrimSpace(key))
		}
	}
	return got
}

func TestCoverage(t *testing.T) {
	paths, err := filepath.Glob(filepath.Join("coverage", "*.yml"))
	if err != nil || len(paths) == 0 {
		t.Fatalf("no manifest in coverage/: %v", err)
	}

	var all tally
	referred := map[string]bool{}
	report := []string{"writing rules checked by the style"}
	for _, path := range paths {
		got := readManifest(t, path, referred)
		all.checked += got.checked
		all.total += got.total
		report = append(report, fmt.Sprintf("  %-16s %s", filepath.Base(path), got))
	}
	report = append(report, fmt.Sprintf("  %-16s %s", "total", all))
	t.Log(strings.Join(report, "\n"))

	rules, err := filepath.Glob(filepath.Join("styles", "Micllam", "*.yml"))
	if err != nil {
		t.Fatal(err)
	}
	for _, rule := range rules {
		if !referred[rule] {
			t.Errorf("no manifest in coverage/ refers to %s", rule)
		}
	}
}

// A rule of docs/agent-guide.md: a list item with a bold lead-in that ends in
// a full stop.
var guideRule = regexp.MustCompile(`(?m)^- \*\*([^*]+)\.\*\* `)

func TestAgentGuideStatesTheUncheckedRules(t *testing.T) {
	paths, err := filepath.Glob(filepath.Join("coverage", "*.yml"))
	if err != nil || len(paths) == 0 {
		t.Fatalf("no manifest in coverage/: %v", err)
	}
	unchecked := map[string]bool{}
	for _, path := range paths {
		for _, key := range readManifest(t, path, map[string]bool{}).unchecked {
			unchecked[key] = true
		}
	}

	guide, err := os.ReadFile(filepath.Join("docs", "agent-guide.md"))
	if err != nil {
		t.Fatal(err)
	}
	stated := map[string]bool{}
	for _, m := range guideRule.FindAllStringSubmatch(string(guide), -1) {
		stated[anchor(m[1])] = true
	}

	for key := range unchecked {
		if !stated[key] {
			t.Errorf("docs/agent-guide.md does not state %s", key)
		}
	}
	for key := range stated {
		if !unchecked[key] {
			t.Errorf("docs/agent-guide.md states %s, which is not an unchecked key of coverage/", key)
		}
	}
}
