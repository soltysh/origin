// Code generated by protoc-gen-gogo.
// source: github.com/openshift/origin/vendor/k8s.io/apimachinery/pkg/util/intstr/generated.proto
// DO NOT EDIT!

/*
	Package intstr is a generated protocol buffer package.

	It is generated from these files:
		github.com/openshift/origin/vendor/k8s.io/apimachinery/pkg/util/intstr/generated.proto

	It has these top-level messages:
		IntOrString
*/
package intstr

import proto "github.com/gogo/protobuf/proto"
import fmt "fmt"
import math "math"

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

func (m *IntOrString) Reset()                    { *m = IntOrString{} }
func (*IntOrString) ProtoMessage()               {}
func (*IntOrString) Descriptor() ([]byte, []int) { return fileDescriptorGenerated, []int{0} }

func init() {
	proto.RegisterType((*IntOrString)(nil), "k8s.io.apimachinery.pkg.util.intstr.IntOrString")
}
func (m *IntOrString) Marshal() (dAtA []byte, err error) {
	size := m.Size()
	dAtA = make([]byte, size)
	n, err := m.MarshalTo(dAtA)
	if err != nil {
		return nil, err
	}
	return dAtA[:n], nil
}

func (m *IntOrString) MarshalTo(dAtA []byte) (int, error) {
	var i int
	_ = i
	var l int
	_ = l
	dAtA[i] = 0x8
	i++
	i = encodeVarintGenerated(dAtA, i, uint64(m.Type))
	dAtA[i] = 0x10
	i++
	i = encodeVarintGenerated(dAtA, i, uint64(m.IntVal))
	dAtA[i] = 0x1a
	i++
	i = encodeVarintGenerated(dAtA, i, uint64(len(m.StrVal)))
	i += copy(dAtA[i:], m.StrVal)
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
func (m *IntOrString) Size() (n int) {
	var l int
	_ = l
	n += 1 + sovGenerated(uint64(m.Type))
	n += 1 + sovGenerated(uint64(m.IntVal))
	l = len(m.StrVal)
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
func (m *IntOrString) Unmarshal(dAtA []byte) error {
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
			return fmt.Errorf("proto: IntOrString: wiretype end group for non-group")
		}
		if fieldNum <= 0 {
			return fmt.Errorf("proto: IntOrString: illegal tag %d (wire type %d)", fieldNum, wire)
		}
		switch fieldNum {
		case 1:
			if wireType != 0 {
				return fmt.Errorf("proto: wrong wireType = %d for field Type", wireType)
			}
			m.Type = 0
			for shift := uint(0); ; shift += 7 {
				if shift >= 64 {
					return ErrIntOverflowGenerated
				}
				if iNdEx >= l {
					return io.ErrUnexpectedEOF
				}
				b := dAtA[iNdEx]
				iNdEx++
				m.Type |= (Type(b) & 0x7F) << shift
				if b < 0x80 {
					break
				}
			}
		case 2:
			if wireType != 0 {
				return fmt.Errorf("proto: wrong wireType = %d for field IntVal", wireType)
			}
			m.IntVal = 0
			for shift := uint(0); ; shift += 7 {
				if shift >= 64 {
					return ErrIntOverflowGenerated
				}
				if iNdEx >= l {
					return io.ErrUnexpectedEOF
				}
				b := dAtA[iNdEx]
				iNdEx++
				m.IntVal |= (int32(b) & 0x7F) << shift
				if b < 0x80 {
					break
				}
			}
		case 3:
			if wireType != 2 {
				return fmt.Errorf("proto: wrong wireType = %d for field StrVal", wireType)
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
			m.StrVal = string(dAtA[iNdEx:postIndex])
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
	proto.RegisterFile("github.com/openshift/origin/vendor/k8s.io/apimachinery/pkg/util/intstr/generated.proto", fileDescriptorGenerated)
}

var fileDescriptorGenerated = []byte{
	// 296 bytes of a gzipped FileDescriptorProto
	0x1f, 0x8b, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0xff, 0x4c, 0x8f, 0xb1, 0x4e, 0xeb, 0x30,
	0x14, 0x86, 0xed, 0xdb, 0xde, 0x0a, 0x82, 0xc4, 0x50, 0x31, 0x54, 0x0c, 0x6e, 0x04, 0x12, 0xca,
	0x00, 0xf6, 0x8a, 0x18, 0xbb, 0x75, 0x42, 0x6a, 0x51, 0x07, 0xb6, 0xb4, 0x75, 0x1d, 0x2b, 0xad,
	0x6d, 0x39, 0x27, 0x48, 0xd9, 0xfa, 0x08, 0xb0, 0x31, 0xf2, 0x38, 0x19, 0x3b, 0x76, 0x40, 0x15,
	0x31, 0x6f, 0xc1, 0x84, 0xe2, 0x44, 0xa2, 0x93, 0x7d, 0xfe, 0xff, 0xfb, 0x6c, 0x9d, 0x60, 0x26,
	0x24, 0x24, 0xf9, 0x9c, 0x2e, 0xf4, 0x86, 0x69, 0xc3, 0x55, 0x96, 0xc8, 0x15, 0x30, 0x6d, 0xa5,
	0x90, 0x8a, 0xbd, 0x70, 0xb5, 0xd4, 0x96, 0xa5, 0xf7, 0x19, 0x95, 0x9a, 0xc5, 0x46, 0x6e, 0xe2,
	0x45, 0x22, 0x15, 0xb7, 0x05, 0x33, 0xa9, 0x60, 0x39, 0xc8, 0x35, 0x93, 0x0a, 0x32, 0xb0, 0x4c,
	0x70, 0xc5, 0x6d, 0x0c, 0x7c, 0x49, 0x8d, 0xd5, 0xa0, 0xfb, 0xd7, 0x8d, 0x44, 0x8f, 0x25, 0x6a,
	0x52, 0x41, 0x6b, 0x89, 0x36, 0xd2, 0xe5, 0xdd, 0xd1, 0xe7, 0x42, 0x0b, 0xcd, 0xbc, 0x3b, 0xcf,
	0x57, 0x7e, 0xf2, 0x83, 0xbf, 0x35, 0x6f, 0x5e, 0xbd, 0xe1, 0xe0, 0x6c, 0xac, 0xe0, 0xd1, 0x4e,
	0xc1, 0x4a, 0x25, 0xfa, 0x51, 0xd0, 0x85, 0xc2, 0xf0, 0x01, 0x0e, 0x71, 0xd4, 0x19, 0x5d, 0x94,
	0x87, 0x21, 0x72, 0x87, 0x61, 0xf7, 0xa9, 0x30, 0xfc, 0xa7, 0x3d, 0x27, 0x9e, 0xe8, 0xdf, 0x04,
	0x3d, 0xa9, 0x60, 0x16, 0xaf, 0x07, 0xff, 0x42, 0x1c, 0xfd, 0x1f, 0x9d, 0xb7, 0x6c, 0x6f, 0xec,
	0xd3, 0x49, 0xdb, 0xd6, 0x5c, 0x06, 0xb6, 0xe6, 0x3a, 0x21, 0x8e, 0x4e, 0xff, 0xb8, 0xa9, 0x4f,
	0x27, 0x6d, 0xfb, 0x70, 0xf2, 0xfe, 0x31, 0x44, 0xdb, 0xcf, 0x10, 0x8d, 0x6e, 0xcb, 0x8a, 0xa0,
	0x5d, 0x45, 0xd0, 0xbe, 0x22, 0x68, 0xeb, 0x08, 0x2e, 0x1d, 0xc1, 0x3b, 0x47, 0xf0, 0xde, 0x11,
	0xfc, 0xe5, 0x08, 0x7e, 0xfd, 0x26, 0xe8, 0xb9, 0xd7, 0x2c, 0xfc, 0x1b, 0x00, 0x00, 0xff, 0xff,
	0xa1, 0xb4, 0xab, 0x95, 0x6e, 0x01, 0x00, 0x00,
}
