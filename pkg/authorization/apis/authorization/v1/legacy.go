package v1

func init() {
	// TODO: Remove this once the legacy API will be deprecated. We need this now
	// in order to make the serialization test pass.
	LegacySchemeBuilder.Register(RegisterConversions)
}
