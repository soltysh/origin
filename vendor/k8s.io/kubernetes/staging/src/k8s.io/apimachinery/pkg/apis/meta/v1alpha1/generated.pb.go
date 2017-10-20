// Code generated by protoc-gen-gogo.
// source: github.com/openshift/origin/vendor/k8s.io/apimachinery/pkg/apis/meta/v1alpha1/generated.proto
// DO NOT EDIT!

/*
	Package v1alpha1 is a generated protocol buffer package.

	It is generated from these files:
		github.com/openshift/origin/vendor/k8s.io/apimachinery/pkg/apis/meta/v1alpha1/generated.proto

	It has these top-level messages:
		PartialObjectMetadata
		PartialObjectMetadataList
		TableOptions
*/
package v1alpha1

import proto "github.com/gogo/protobuf/proto"
import fmt "fmt"
import math "math"

import strings "strings"
import reflect "reflect"

import io "io"

// Reference imports to suppress errors if they are not otherwise used.
var _ = proto.Marshal
var _ = fmt.Errorf
var _ = math.Inf

// This is a compile-time assertion to ensure that this generated file
// is compatible with the proto package it is being compiled against.
// A compilation error at this line likely means your copy of the
// proto package needs to be updated.
const _ = proto.GoGoProtoPackageIsVersion2 // please upgrade the proto package

func (m *PartialObjectMetadata) Reset()                    { *m = PartialObjectMetadata{} }
func (*PartialObjectMetadata) ProtoMessage()               {}
func (*PartialObjectMetadata) Descriptor() ([]byte, []int) { return fileDescriptorGenerated, []int{0} }

func (m *PartialObjectMetadataList) Reset()      { *m = PartialObjectMetadataList{} }
func (*PartialObjectMetadataList) ProtoMessage() {}
func (*PartialObjectMetadataList) Descriptor() ([]byte, []int) {
	return fileDescriptorGenerated, []int{1}
}

func (m *TableOptions) Reset()                    { *m = TableOptions{} }
func (*TableOptions) ProtoMessage()               {}
func (*TableOptions) Descriptor() ([]byte, []int) { return fileDescriptorGenerated, []int{2} }

func init() {
	proto.RegisterType((*PartialObjectMetadata)(nil), "k8s.io.apimachinery.pkg.apis.meta.v1alpha1.PartialObjectMetadata")
	proto.RegisterType((*PartialObjectMetadataList)(nil), "k8s.io.apimachinery.pkg.apis.meta.v1alpha1.PartialObjectMetadataList")
	proto.RegisterType((*TableOptions)(nil), "k8s.io.apimachinery.pkg.apis.meta.v1alpha1.TableOptions")
}
func (m *PartialObjectMetadata) Marshal() (dAtA []byte, err error) {
	size := m.Size()
	dAtA = make([]byte, size)
	n, err := m.MarshalTo(dAtA)
	if err != nil {
		return nil, err
	}
	return dAtA[:n], nil
}

func (m *PartialObjectMetadata) MarshalTo(dAtA []byte) (int, error) {
	var i int
	_ = i
	var l int
	_ = l
	dAtA[i] = 0xa
	i++
	i = encodeVarintGenerated(dAtA, i, uint64(m.ObjectMeta.Size()))
	n1, err := m.ObjectMeta.MarshalTo(dAtA[i:])
	if err != nil {
		return 0, err
	}
	i += n1
	return i, nil
}

func (m *PartialObjectMetadataList) Marshal() (dAtA []byte, err error) {
	size := m.Size()
	dAtA = make([]byte, size)
	n, err := m.MarshalTo(dAtA)
	if err != nil {
		return nil, err
	}
	return dAtA[:n], nil
}

func (m *PartialObjectMetadataList) MarshalTo(dAtA []byte) (int, error) {
	var i int
	_ = i
	var l int
	_ = l
	if len(m.Items) > 0 {
		for _, msg := range m.Items {
			dAtA[i] = 0xa
			i++
			i = encodeVarintGenerated(dAtA, i, uint64(msg.Size()))
			n, err := msg.MarshalTo(dAtA[i:])
			if err != nil {
				return 0, err
			}
			i += n
		}
	}
	return i, nil
}

func (m *TableOptions) Marshal() (dAtA []byte, err error) {
	size := m.Size()
	dAtA = make([]byte, size)
	n, err := m.MarshalTo(dAtA)
	if err != nil {
		return nil, err
	}
	return dAtA[:n], nil
}

func (m *TableOptions) MarshalTo(dAtA []byte) (int, error) {
	var i int
	_ = i
	var l int
	_ = l
	dAtA[i] = 0xa
	i++
	i = encodeVarintGenerated(dAtA, i, uint64(len(m.IncludeObject)))
	i += copy(dAtA[i:], m.IncludeObject)
	return i, nil
}

func encodeFixed64Generated(dAtA []byte, offset int, v uint64) int {
	dAtA[offset] = uint8(v)
	dAtA[offset+1] = uint8(v >> 8)
	dAtA[offset+2] = uint8(v >> 16)
	dAtA[offset+3] = uint8(v >> 24)
	dAtA[offset+4] = uint8(v >> 32)
	dAtA[offset+5] = uint8(v >> 40)
	dAtA[offset+6] = uint8(v >> 48)
	dAtA[offset+7] = uint8(v >> 56)
	return offset + 8
}
func encodeFixed32Generated(dAtA []byte, offset int, v uint32) int {
	dAtA[offset] = uint8(v)
	dAtA[offset+1] = uint8(v >> 8)
	dAtA[offset+2] = uint8(v >> 16)
	dAtA[offset+3] = uint8(v >> 24)
	return offset + 4
}
func encodeVarintGenerated(dAtA []byte, offset int, v uint64) int {
	for v >= 1<<7 {
		dAtA[offset] = uint8(v&0x7f | 0x80)
		v >>= 7
		offset++
	}
	dAtA[offset] = uint8(v)
	return offset + 1
}
func (m *PartialObjectMetadata) Size() (n int) {
	var l int
	_ = l
	l = m.ObjectMeta.Size()
	n += 1 + l + sovGenerated(uint64(l))
	return n
}

func (m *PartialObjectMetadataList) Size() (n int) {
	var l int
	_ = l
	if len(m.Items) > 0 {
		for _, e := range m.Items {
			l = e.Size()
			n += 1 + l + sovGenerated(uint64(l))
		}
	}
	return n
}

func (m *TableOptions) Size() (n int) {
	var l int
	_ = l
	l = len(m.IncludeObject)
	n += 1 + l + sovGenerated(uint64(l))
	return n
}

func sovGenerated(x uint64) (n int) {
	for {
		n++
		x >>= 7
		if x == 0 {
			break
		}
	}
	return n
}
func sozGenerated(x uint64) (n int) {
	return sovGenerated(uint64((x << 1) ^ uint64((int64(x) >> 63))))
}
func (this *PartialObjectMetadata) String() string {
	if this == nil {
		return "nil"
	}
	s := strings.Join([]string{`&PartialObjectMetadata{`,
		`ObjectMeta:` + strings.Replace(strings.Replace(this.ObjectMeta.String(), "ObjectMeta", "k8s_io_apimachinery_pkg_apis_meta_v1.ObjectMeta", 1), `&`, ``, 1) + `,`,
		`}`,
	}, "")
	return s
}
func (this *PartialObjectMetadataList) String() string {
	if this == nil {
		return "nil"
	}
	s := strings.Join([]string{`&PartialObjectMetadataList{`,
		`Items:` + strings.Replace(fmt.Sprintf("%v", this.Items), "PartialObjectMetadata", "PartialObjectMetadata", 1) + `,`,
		`}`,
	}, "")
	return s
}
func (this *TableOptions) String() string {
	if this == nil {
		return "nil"
	}
	s := strings.Join([]string{`&TableOptions{`,
		`IncludeObject:` + fmt.Sprintf("%v", this.IncludeObject) + `,`,
		`}`,
	}, "")
	return s
}
func valueToStringGenerated(v interface{}) string {
	rv := reflect.ValueOf(v)
	if rv.IsNil() {
		return "nil"
	}
	pv := reflect.Indirect(rv).Interface()
	return fmt.Sprintf("*%v", pv)
}
func (m *PartialObjectMetadata) Unmarshal(dAtA []byte) error {
	l := len(dAtA)
	iNdEx := 0
	for iNdEx < l {
		preIndex := iNdEx
		var wire uint64
		for shift := uint(0); ; shift += 7 {
			if shift >= 64 {
				return ErrIntOverflowGenerated
			}
			if iNdEx >= l {
				return io.ErrUnexpectedEOF
			}
			b := dAtA[iNdEx]
			iNdEx++
			wire |= (uint64(b) & 0x7F) << shift
			if b < 0x80 {
				break
			}
		}
		fieldNum := int32(wire >> 3)
		wireType := int(wire & 0x7)
		if wireType == 4 {
			return fmt.Errorf("proto: PartialObjectMetadata: wiretype end group for non-group")
		}
		if fieldNum <= 0 {
			return fmt.Errorf("proto: PartialObjectMetadata: illegal tag %d (wire type %d)", fieldNum, wire)
		}
		switch fieldNum {
		case 1:
			if wireType != 2 {
				return fmt.Errorf("proto: wrong wireType = %d for field ObjectMeta", wireType)
			}
			var msglen int
			for shift := uint(0); ; shift += 7 {
				if shift >= 64 {
					return ErrIntOverflowGenerated
				}
				if iNdEx >= l {
					return io.ErrUnexpectedEOF
				}
				b := dAtA[iNdEx]
				iNdEx++
				msglen |= (int(b) & 0x7F) << shift
				if b < 0x80 {
					break
				}
			}
			if msglen < 0 {
				return ErrInvalidLengthGenerated
			}
			postIndex := iNdEx + msglen
			if postIndex > l {
				return io.ErrUnexpectedEOF
			}
			if err := m.ObjectMeta.Unmarshal(dAtA[iNdEx:postIndex]); err != nil {
				return err
			}
			iNdEx = postIndex
		default:
			iNdEx = preIndex
			skippy, err := skipGenerated(dAtA[iNdEx:])
			if err != nil {
				return err
			}
			if skippy < 0 {
				return ErrInvalidLengthGenerated
			}
			if (iNdEx + skippy) > l {
				return io.ErrUnexpectedEOF
			}
			iNdEx += skippy
		}
	}

	if iNdEx > l {
		return io.ErrUnexpectedEOF
	}
	return nil
}
func (m *PartialObjectMetadataList) Unmarshal(dAtA []byte) error {
	l := len(dAtA)
	iNdEx := 0
	for iNdEx < l {
		preIndex := iNdEx
		var wire uint64
		for shift := uint(0); ; shift += 7 {
			if shift >= 64 {
				return ErrIntOverflowGenerated
			}
			if iNdEx >= l {
				return io.ErrUnexpectedEOF
			}
			b := dAtA[iNdEx]
			iNdEx++
			wire |= (uint64(b) & 0x7F) << shift
			if b < 0x80 {
				break
			}
		}
		fieldNum := int32(wire >> 3)
		wireType := int(wire & 0x7)
		if wireType == 4 {
			return fmt.Errorf("proto: PartialObjectMetadataList: wiretype end group for non-group")
		}
		if fieldNum <= 0 {
			return fmt.Errorf("proto: PartialObjectMetadataList: illegal tag %d (wire type %d)", fieldNum, wire)
		}
		switch fieldNum {
		case 1:
			if wireType != 2 {
				return fmt.Errorf("proto: wrong wireType = %d for field Items", wireType)
			}
			var msglen int
			for shift := uint(0); ; shift += 7 {
				if shift >= 64 {
					return ErrIntOverflowGenerated
				}
				if iNdEx >= l {
					return io.ErrUnexpectedEOF
				}
				b := dAtA[iNdEx]
				iNdEx++
				msglen |= (int(b) & 0x7F) << shift
				if b < 0x80 {
					break
				}
			}
			if msglen < 0 {
				return ErrInvalidLengthGenerated
			}
			postIndex := iNdEx + msglen
			if postIndex > l {
				return io.ErrUnexpectedEOF
			}
			m.Items = append(m.Items, &PartialObjectMetadata{})
			if err := m.Items[len(m.Items)-1].Unmarshal(dAtA[iNdEx:postIndex]); err != nil {
				return err
			}
			iNdEx = postIndex
		default:
			iNdEx = preIndex
			skippy, err := skipGenerated(dAtA[iNdEx:])
			if err != nil {
				return err
			}
			if skippy < 0 {
				return ErrInvalidLengthGenerated
			}
			if (iNdEx + skippy) > l {
				return io.ErrUnexpectedEOF
			}
			iNdEx += skippy
		}
	}

	if iNdEx > l {
		return io.ErrUnexpectedEOF
	}
	return nil
}
func (m *TableOptions) Unmarshal(dAtA []byte) error {
	l := len(dAtA)
	iNdEx := 0
	for iNdEx < l {
		preIndex := iNdEx
		var wire uint64
		for shift := uint(0); ; shift += 7 {
			if shift >= 64 {
				return ErrIntOverflowGenerated
			}
			if iNdEx >= l {
				return io.ErrUnexpectedEOF
			}
			b := dAtA[iNdEx]
			iNdEx++
			wire |= (uint64(b) & 0x7F) << shift
			if b < 0x80 {
				break
			}
		}
		fieldNum := int32(wire >> 3)
		wireType := int(wire & 0x7)
		if wireType == 4 {
			return fmt.Errorf("proto: TableOptions: wiretype end group for non-group")
		}
		if fieldNum <= 0 {
			return fmt.Errorf("proto: TableOptions: illegal tag %d (wire type %d)", fieldNum, wire)
		}
		switch fieldNum {
		case 1:
			if wireType != 2 {
				return fmt.Errorf("proto: wrong wireType = %d for field IncludeObject", wireType)
			}
			var stringLen uint64
			for shift := uint(0); ; shift += 7 {
				if shift >= 64 {
					return ErrIntOverflowGenerated
				}
				if iNdEx >= l {
					return io.ErrUnexpectedEOF
				}
				b := dAtA[iNdEx]
				iNdEx++
				stringLen |= (uint64(b) & 0x7F) << shift
				if b < 0x80 {
					break
				}
			}
			intStringLen := int(stringLen)
			if intStringLen < 0 {
				return ErrInvalidLengthGenerated
			}
			postIndex := iNdEx + intStringLen
			if postIndex > l {
				return io.ErrUnexpectedEOF
			}
			m.IncludeObject = IncludeObjectPolicy(dAtA[iNdEx:postIndex])
			iNdEx = postIndex
		default:
			iNdEx = preIndex
			skippy, err := skipGenerated(dAtA[iNdEx:])
			if err != nil {
				return err
			}
			if skippy < 0 {
				return ErrInvalidLengthGenerated
			}
			if (iNdEx + skippy) > l {
				return io.ErrUnexpectedEOF
			}
			iNdEx += skippy
		}
	}

	if iNdEx > l {
		return io.ErrUnexpectedEOF
	}
	return nil
}
func skipGenerated(dAtA []byte) (n int, err error) {
	l := len(dAtA)
	iNdEx := 0
	for iNdEx < l {
		var wire uint64
		for shift := uint(0); ; shift += 7 {
			if shift >= 64 {
				return 0, ErrIntOverflowGenerated
			}
			if iNdEx >= l {
				return 0, io.ErrUnexpectedEOF
			}
			b := dAtA[iNdEx]
			iNdEx++
			wire |= (uint64(b) & 0x7F) << shift
			if b < 0x80 {
				break
			}
		}
		wireType := int(wire & 0x7)
		switch wireType {
		case 0:
			for shift := uint(0); ; shift += 7 {
				if shift >= 64 {
					return 0, ErrIntOverflowGenerated
				}
				if iNdEx >= l {
					return 0, io.ErrUnexpectedEOF
				}
				iNdEx++
				if dAtA[iNdEx-1] < 0x80 {
					break
				}
			}
			return iNdEx, nil
		case 1:
			iNdEx += 8
			return iNdEx, nil
		case 2:
			var length int
			for shift := uint(0); ; shift += 7 {
				if shift >= 64 {
					return 0, ErrIntOverflowGenerated
				}
				if iNdEx >= l {
					return 0, io.ErrUnexpectedEOF
				}
				b := dAtA[iNdEx]
				iNdEx++
				length |= (int(b) & 0x7F) << shift
				if b < 0x80 {
					break
				}
			}
			iNdEx += length
			if length < 0 {
				return 0, ErrInvalidLengthGenerated
			}
			return iNdEx, nil
		case 3:
			for {
				var innerWire uint64
				var start int = iNdEx
				for shift := uint(0); ; shift += 7 {
					if shift >= 64 {
						return 0, ErrIntOverflowGenerated
					}
					if iNdEx >= l {
						return 0, io.ErrUnexpectedEOF
					}
					b := dAtA[iNdEx]
					iNdEx++
					innerWire |= (uint64(b) & 0x7F) << shift
					if b < 0x80 {
						break
					}
				}
				innerWireType := int(innerWire & 0x7)
				if innerWireType == 4 {
					break
				}
				next, err := skipGenerated(dAtA[start:])
				if err != nil {
					return 0, err
				}
				iNdEx = start + next
			}
			return iNdEx, nil
		case 4:
			return iNdEx, nil
		case 5:
			iNdEx += 4
			return iNdEx, nil
		default:
			return 0, fmt.Errorf("proto: illegal wireType %d", wireType)
		}
	}
	panic("unreachable")
}

var (
	ErrInvalidLengthGenerated = fmt.Errorf("proto: negative length found during unmarshaling")
	ErrIntOverflowGenerated   = fmt.Errorf("proto: integer overflow")
)

func init() {
	proto.RegisterFile("github.com/openshift/origin/vendor/k8s.io/apimachinery/pkg/apis/meta/v1alpha1/generated.proto", fileDescriptorGenerated)
}

var fileDescriptorGenerated = []byte{
	// 397 bytes of a gzipped FileDescriptorProto
	0x1f, 0x8b, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0xff, 0x8c, 0x91, 0xcf, 0x6b, 0xd4, 0x40,
	0x14, 0xc7, 0x33, 0x48, 0xa1, 0x9d, 0xda, 0x4b, 0x44, 0xa8, 0x7b, 0x98, 0x94, 0x3d, 0x15, 0xd1,
	0x19, 0x5b, 0x45, 0xbc, 0x9a, 0x5b, 0x41, 0x69, 0x09, 0x9e, 0x04, 0xc1, 0x49, 0x32, 0x4d, 0x9e,
	0x9b, 0xcc, 0x84, 0x99, 0x97, 0xc2, 0x9e, 0xf4, 0x4f, 0xf0, 0xcf, 0xda, 0x63, 0x8f, 0x3d, 0x05,
	0x37, 0xfe, 0x17, 0x9e, 0x24, 0x49, 0x6b, 0xb7, 0xfb, 0x03, 0xf7, 0xf6, 0xde, 0x37, 0x7c, 0x3e,
	0xf9, 0xbe, 0x84, 0x7e, 0xc9, 0x00, 0xf3, 0x3a, 0xe6, 0x89, 0x29, 0x85, 0xa9, 0x94, 0x76, 0x39,
	0x5c, 0xa2, 0x30, 0x16, 0x32, 0xd0, 0xe2, 0x4a, 0xe9, 0xd4, 0x58, 0x31, 0x79, 0xe7, 0x38, 0x18,
	0x21, 0x2b, 0x28, 0x65, 0x92, 0x83, 0x56, 0x76, 0x2a, 0xaa, 0x49, 0xd6, 0x05, 0x4e, 0x94, 0x0a,
	0xa5, 0xb8, 0x3a, 0x91, 0x45, 0x95, 0xcb, 0x13, 0x91, 0x29, 0xad, 0xac, 0x44, 0x95, 0xf2, 0xca,
	0x1a, 0x34, 0xfe, 0xf3, 0x81, 0xe5, 0x8b, 0x2c, 0xaf, 0x26, 0x59, 0x17, 0x38, 0xde, 0xb1, 0xfc,
	0x8e, 0x1d, 0xbd, 0x5c, 0xa8, 0x92, 0x99, 0xcc, 0x88, 0x5e, 0x11, 0xd7, 0x97, 0xfd, 0xd6, 0x2f,
	0xfd, 0x34, 0xa8, 0x47, 0x6f, 0xb6, 0xa9, 0xb5, 0x5c, 0x68, 0xb4, 0xf1, 0x18, 0x5b, 0x6b, 0x84,
	0x52, 0xad, 0x00, 0x6f, 0xff, 0x07, 0xb8, 0x24, 0x57, 0xa5, 0x5c, 0xe1, 0x5e, 0x6f, 0xe2, 0x6a,
	0x84, 0x42, 0x80, 0x46, 0x87, 0x76, 0x19, 0x1a, 0x4f, 0xe9, 0xd3, 0x0b, 0x69, 0x11, 0x64, 0x71,
	0x1e, 0x7f, 0x53, 0x09, 0x7e, 0x54, 0x28, 0x53, 0x89, 0xd2, 0xff, 0x4a, 0x77, 0xcb, 0xdb, 0xf9,
	0x90, 0x1c, 0x91, 0xe3, 0xfd, 0xd3, 0x57, 0x7c, 0x9b, 0x4f, 0xcb, 0xef, 0x3d, 0xa1, 0x3f, 0x6b,
	0x02, 0xaf, 0x6d, 0x02, 0x7a, 0x9f, 0x45, 0xff, 0xac, 0xe3, 0xef, 0xf4, 0xd9, 0xda, 0x57, 0x7f,
	0x00, 0x87, 0x7e, 0x4c, 0x77, 0x00, 0x55, 0xe9, 0x0e, 0xc9, 0xd1, 0xa3, 0xe3, 0xfd, 0xd3, 0xf7,
	0x7c, 0xfb, 0xdf, 0xca, 0xd7, 0x5a, 0xc3, 0xbd, 0xb6, 0x09, 0x76, 0xce, 0x3a, 0x67, 0x34, 0xa8,
	0xc7, 0x31, 0x7d, 0xfc, 0x49, 0xc6, 0x85, 0x3a, 0xaf, 0x10, 0x8c, 0x76, 0x7e, 0x44, 0x0f, 0x40,
	0x27, 0x45, 0x9d, 0xaa, 0x01, 0xed, 0xef, 0xde, 0x0b, 0x5f, 0xdc, 0x5e, 0x71, 0x70, 0xb6, 0xf8,
	0xf0, 0x4f, 0x13, 0x3c, 0x79, 0x10, 0x5c, 0x98, 0x02, 0x92, 0x69, 0xf4, 0x50, 0x11, 0xf2, 0xd9,
	0x9c, 0x79, 0xd7, 0x73, 0xe6, 0xdd, 0xcc, 0x99, 0xf7, 0xa3, 0x65, 0x64, 0xd6, 0x32, 0x72, 0xdd,
	0x32, 0x72, 0xd3, 0x32, 0xf2, 0xab, 0x65, 0xe4, 0xe7, 0x6f, 0xe6, 0x7d, 0xde, 0xbd, 0xeb, 0xfe,
	0x37, 0x00, 0x00, 0xff, 0xff, 0x5b, 0xb9, 0xb4, 0x5c, 0x1e, 0x03, 0x00, 0x00,
}
