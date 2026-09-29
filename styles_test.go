package writingkit

import (
	"bytes"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"testing"
)

var linkLine = regexp.MustCompile(`(?m)^link: .*/docs/writing-style\.md#([a-z0-9-]+)$`)

// The anchor of a heading on GitHub: lowercase, with spaces as hyphens and
// punctuation removed.
func anchor(heading string) string {
	var b strings.Builder
	for _, r := range strings.ToLower(heading) {
		switch {
		case r >= 'a' && r <= 'z', r >= '0' && r <= '9', r == '-':
			b.WriteRune(r)
		case r == ' ':
			b.WriteRune('-')
		}
	}
	return b.String()
}

func TestRuleLinksToASectionOfTheStyle(t *testing.T) {
	style, err := os.ReadFile(filepath.Join("docs", "writing-style.md"))
	if err != nil {
		t.Fatal(err)
	}
	sections := map[string]bool{}
	for _, line := range strings.Split(string(style), "\n") {
		if heading, ok := strings.CutPrefix(line, "## "); ok {
			sections[anchor(heading)] = true
		}
	}

	rules, err := filepath.Glob(filepath.Join("styles", "Micllam", "*.yml"))
	if err != nil || len(rules) == 0 {
		t.Fatalf("no rule in styles/Micllam: %v", err)
	}
	for _, rule := range rules {
		data, err := os.ReadFile(rule)
		if err != nil {
			t.Fatal(err)
		}
		m := linkLine.FindSubmatch(data)
		if m == nil {
			t.Errorf("%s has no link to docs/writing-style.md", rule)
			continue
		}
		if !sections[string(m[1])] {
			t.Errorf("%s links to #%s, which is not a section of docs/writing-style.md", rule, m[1])
		}
	}
}

// WrapComments.tengo and WrapMarkdown.tengo differ in their first line only,
// which sets the mode.
func TestWrapScriptsAreTwins(t *testing.T) {
	read := func(name string) []byte {
		data, err := os.ReadFile(filepath.Join("styles", "config", "scripts", name))
		if err != nil {
			t.Fatal(err)
		}
		_, rest, _ := bytes.Cut(data, []byte("\n"))
		return rest
	}
	if !bytes.Equal(read("WrapComments.tengo"), read("WrapMarkdown.tengo")) {
		t.Error("WrapComments.tengo and WrapMarkdown.tengo differ after their first line")
	}
}
