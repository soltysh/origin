package digest

import (
	"crypto"
	"hash"

	"github.com/opencontainers/go-digest"
)

// Algorithm identifies and implementation of a digester by an identifier.
// Note the that this defines both the hash algorithm used and the string
// encoding.
type Algorithm = digest.Algorithm

// supported digest types
const (
	SHA256 Algorithm = "sha256" // sha256 with hex encoding
	SHA384 Algorithm = "sha384" // sha384 with hex encoding
	SHA512 Algorithm = "sha512" // sha512 with hex encoding

	// Canonical is the primary digest algorithm used with the distribution
	// project. Other digests may be used but this one is the primary storage
	// digest.
	Canonical = SHA256
)

var (
	// TODO(stevvooe): Follow the pattern of the standard crypto package for
	// registration of digests. Effectively, we are a registerable set and
	// common symbol access.

	// algorithms maps values to hash.Hash implementations. Other algorithms
	// may be available but they cannot be calculated by the digest package.
	algorithms = map[Algorithm]crypto.Hash{
		SHA256: crypto.SHA256,
		SHA384: crypto.SHA384,
		SHA512: crypto.SHA512,
	}
)

// TODO(stevvooe): Allow resolution of verifiers using the digest type and
// this registration system.

// Digester calculates the digest of written data. Writes should go directly
// to the return value of Hash, while calling Digest will return the current
// value of the digest.
type Digester interface {
	Hash() hash.Hash // provides direct access to underlying hash instance.
	Digest() Digest
}

// digester provides a simple digester definition that embeds a hasher.
type digester struct {
	alg  Algorithm
	hash hash.Hash
}

func (d *digester) Hash() hash.Hash {
	return d.hash
}

func (d *digester) Digest() Digest {
	return NewDigest(d.alg, d.hash)
}
