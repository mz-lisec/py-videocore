'Test of pack/unpack functionality'

from nose.tools import raises
from struct import pack

import videocore.assembler as A
from videocore.assembler import REGISTERS, AssembleError 

#=================================== Register =================================

def test_register_names():
    for name in REGISTERS:
        reg = REGISTERS[name]
        assert(reg.name == name)
        assert(str(reg) == name)

def test_pack_of_regA():
    REGISTERS['ra0'].pack('nop')  # no throw

@raises(AssembleError)
def test_pack_of_regB():
    REGISTERS['rb0'].pack('nop')

def test_unpack_of_regA():
    REGISTERS['ra0'].unpack('nop')  # no throw

def test_unpack_of_r4():
    REGISTERS['r4'].unpack('nop')   # no throw

@raises(AssembleError)
def test_unpack_of_regB():
    REGISTERS['rb0'].unpack('nop')


#============================ Instruction encoding ============================

SAMPLE_ALU_INSN = A.AluInsn(
    sig=0, unpack=1, pm=1, pack=2, cond_add=3, cond_mul=4, sf=1, ws=1,
    waddr_add=53, waddr_mul=12, op_mul=4, op_add=2, raddr_a=33, raddr_b=53,
    add_a=4, add_b=7, mul_a=6, mul_b=2
    )

SAMPLE_BRANCH_INSN = A.BranchInsn(
    sig=0xf, cond_br=13, rel=1, reg=0, raddr_a=27, ws=1, waddr_add=53,
    waddr_mul=12, immediate=0x12345678
    )

SAMPLE_LOAD_INSN = A.LoadInsn(
    sig=0xe, unpack=1, pm=1, pack=2, cond_add=3, cond_mul=4, sf=1, ws=1,
    waddr_add=53, waddr_mul=12, immediate=0x12345678
    )

SAMPLE_SEMA_INSN = A.SemaInsn(
    sig=0xe, unpack=4, pm=1, pack=2, cond_add=3, cond_mul=4, sf=1, ws=1,
    waddr_add=53, waddr_mul=12, sa=1, semaphore=13
    )

def test_bytes_convertion():
    for sample_insn in [SAMPLE_ALU_INSN, SAMPLE_BRANCH_INSN,
                        SAMPLE_LOAD_INSN, SAMPLE_SEMA_INSN]:
        insn = A.Insn.from_bytes(sample_insn.to_bytes())
        assert insn == sample_insn

def test_insn_repr():
    assert repr(SAMPLE_ALU_INSN) == (
            'AluInsn(sig=0x0L, unpack=0x1L, pm=0x1L, pack=0x2L, '
            'cond_add=0x3L, cond_mul=0x4L, sf=0x1L, ws=0x1L, waddr_add=0x35L, '
            'waddr_mul=0xcL, op_mul=0x4L, op_add=0x2L, raddr_a=0x21L, '
            'raddr_b=0x35L, add_a=0x4L, add_b=0x7L, mul_a=0x6L, mul_b=0x2L)'
            )