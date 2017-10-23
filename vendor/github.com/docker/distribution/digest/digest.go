package digest

import (
	"fmt"
	"hash"
	"io"
	"regexp"

	"github.com/opencontainers/go-digest"
)

const (
	// DigestSha256EmptyTar is the canonical sha256 digest of empty data
	DigestSha256EmptyTar = "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)

// Digest allows simple protection of hex formatted digest strings, prefixed
// by their algorithm. Strings of type Digest have some guarantee of being in
// the correct format and it provides quick access to the components of a
// digest string.
//
// The following is an example of the contents of Digest types:
//
// 	sha256:7173b809ca12ec5dee4506cd86be934c4596dd234ee82c0662eac04a8c2c71dc
//
// This allows to abstract the digest behind this type and work only in those
// terms.
type Digest = digest.Digest

// NewDigest returns a Digest from alg and a hash.Hash object.
func NewDigest(alg Algorithm, h hash.Hash) Digest {
	return NewDigestFromBytes(alg, h.Sum(nil))
}

// NewDigestFromBytes returns a new digest from the byte contents of p.
// Typically, this can come from hash.Hash.Sum(...) or xxx.SumXXX(...)
// functions. This is also useful for rebuilding digests from binary
// serializations.
func NewDigestFromBytes(alg Algorithm, p []byte) Digest {
	return Digest(fmt.Sprintf("%s:%x", alg, p))
}

// NewDigestFromHex returns a Digest from alg and a the hex encoded digest.
func NewDigestFromHex(alg, hex string) Digest {
	return Digest(fmt.Sprintf("%s:%s", alg, hex))
}

// DigestRegexp matches valid digest types.
var DigestRegexp = regexp.MustCompile(`[a-zA-Z0-9-_+.]+:[a-fA-F0-9]+`)

// DigestRegexpAnchored matches valid digest types, anchored to the start and end of the match.
var DigestRegexpAnchored = regexp.MustCompile(`^` + DigestRegexp.String() + `$`)

var (
	// ErrDigestInvalidFormat returned when digest format invalid.
	ErrDigestInvalidFormat = fmt.Errorf("invalid checksum digest format")

	// ErrDigestInvalidLength returned when digest has invalid length.
	ErrDigestInvalidLength = fmt.Errorf("invalid checksum digest length")

	// ErrDigestUnsupported returned when the digest algorithm is unsupported.
	ErrDigestUnsupported = fmt.Errorf("unsupported digest algorithm")
)

// ParseDigest parses s and returns the validated digest object. An error will
// be returned if the format is invalid.
func ParseDigest(s string) (Digest, error) {
	d := Digest(s)

	return d, d.Validate()
}

// FromReader returns the most valid digest for the underlying content using
// the canonical digest algorithm.
func FromReader(rd io.Reader) (Digest, error) {
	return Canonical.FromReader(rd)
}

// FromBytes digests the input and returns a Digest.
func FromBytes(p []byte) Digest {
	return Canonical.FromBytes(p)
}

// Validate checks that the contents of d is a valid digest, returning an
// error if not.
