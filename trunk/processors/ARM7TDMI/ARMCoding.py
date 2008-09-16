####################################################################################
#         ___        ___           ___           ___
#        /  /\      /  /\         /  /\         /  /\
#       /  /:/     /  /::\       /  /::\       /  /::\
#      /  /:/     /  /:/\:\     /  /:/\:\     /  /:/\:\
#     /  /:/     /  /:/~/:/    /  /:/~/::\   /  /:/~/:/
#    /  /::\    /__/:/ /:/___ /__/:/ /:/\:\ /__/:/ /:/
#   /__/:/\:\   \  \:\/:::::/ \  \:\/:/__\/ \  \:\/:/
#   \__\/  \:\   \  \::/~~~~   \  \::/       \  \::/
#        \  \:\   \  \:\        \  \:\        \  \:\
#         \  \ \   \  \:\        \  \:\        \  \:\
#          \__\/    \__\/         \__\/         \__\/
#
#   This file is part of TRAP.
#
#   TRAP is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this TRAP; if not, write to the
#   Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA.
#   or see <http://www.gnu.org/licenses/>.
#
#   (c) Luca Fossati, fossati@elet.polimi.it
#
####################################################################################


import trap

#---------------------------------------------------------
# Instruction Encoding
#---------------------------------------------------------
# Lets now start with defining the instructions, i.e. their bitstring and
# mnemonic and their behavior (look at page 68 of the ARM Architecture
# Reference Manual). Note the zero* field: it is a special identifier and it
# means that all those bits have value 0; the same applies for one*
dataProc_imm_shift = trap.MachineCode([('cond', 4), ('zero', 3), ('opcode', 4), ('s', 1), ('rn', 4), ('rd', 4), ('shift_amm', 5), ('shift_op', 2), ('zero', 1), ('rm', 4)])
# All of the register specifiers are indexes in the registry bank REGS,
# with no offset (so we access them directly, REGS[rn])
dataProc_imm_shift.setVarField('rn', ('REGS', 0))
dataProc_imm_shift.setVarField('rd', ('REGS', 0))
dataProc_imm_shift.setVarField('rm', ('REGS', 0))
dataProc_reg_shift = trap.MachineCode([('cond', 4), ('zero', 3), ('opcode', 4), ('s', 1), ('rn', 4), ('rd', 4), ('rs', 4), ('zero', 1), ('shift_op', 2), ('one', 1), ('rm', 4)])
dataProc_reg_shift.setVarField('rn', ('REGS', 0))
dataProc_reg_shift.setVarField('rd', ('REGS', 0))
dataProc_reg_shift.setVarField('rm', ('REGS', 0))
dataProc_reg_shift.setVarField('rs', ('REGS', 0))
dataProc_imm = trap.MachineCode([('cond', 4), ('id', 3), ('opcode', 4), ('s', 1), ('rn', 4), ('rd', 4), ('rotate', 4), ('immediate', 8)])
dataProc_imm.setVarField('rn', ('REGS', 0))
dataProc_imm.setVarField('rd', ('REGS', 0))
dataProc_imm.setBitfield('id', [0, 0, 1])

# TODO: see this category, maybe we can express it in a more general way
move_imm2psr = trap.MachineCode([('cond', 4), ('opcode1', 5), ('r', 1), ('opcode2', 2), ('mask', 4), ('sbo', 4), ('rotate', 4), ('immediate', 8)])

ls_immOff = trap.MachineCode([('cond', 4), ('opcode', 3), ('p', 1), ('u', 1), ('b', 1), ('w', 1), ('l', 1), ('rn', 4), ('rd', 4), ('immediate', 12)])
ls_immOff.setBitfield('opcode', [0, 1, 0])
ls_immOff.setVarField('rn', ('REGS', 0))
ls_immOff.setVarField('rd', ('REGS', 0))
ls_regOff = trap.MachineCode([('cond', 4), ('opcode', 3), ('p', 1), ('u', 1), ('b', 1), ('w', 1), ('l', 1), ('rn', 4), ('rd', 4), ('shift_amm', 5), ('shift_op', 2), ('zero', 1), ('rm', 4)])
ls_regOff.setBitfield('opcode', [0, 1, 1])
ls_regOff.setVarField('rn', ('REGS', 0))
ls_regOff.setVarField('rd', ('REGS', 0))
ls_regOff.setVarField('rm', ('REGS', 0))
lsshb_regOff = trap.MachineCode([('cond', 4), ('opcode0', 3), ('p', 1), ('u', 1), ('i', 1), ('w', 1), ('one', 1), ('rn', 4), ('rd', 4), ('addr_mode0', 4), ('opcode1', 4), ('addr_mode1', 4)])
lsshb_regOff.setBitfield('opcode0', [0, 0, 0])
lsshb_regOff.setVarField('rn', ('REGS', 0))
lsshb_regOff.setVarField('rd', ('REGS', 0))
ls_multiple = trap.MachineCode([('cond', 4), ('opcode', 3), ('p', 1), ('u', 1), ('s', 1), ('w', 1), ('l', 1), ('rn', 4), ('reg_list', 16)])
ls_multiple.setBitfield('opcode', [1, 0, 0])
ls_multiple.setVarField('rn', ('REGS', 0))

branch = trap.MachineCode([('cond', 4), ('opcode', 3), ('l', 1), ('offset', 24)])
branch.setBitfield('opcode', [1, 0, 1])
branch_thumb = trap.MachineCode([('cond', 4), ('opcode0', 8), ('zero', 12), ('opcode1', 4), ('rm', 4)])
branch_thumb.setBitfield('opcode0', [0, 0, 0, 1, 0, 0, 1, 0])
branch_thumb.setBitfield('opcode1', [0, 0, 0, 1])
branch_thumb.setVarField('rm', ('REGS', 0))

multiply = trap.MachineCode([('cond', 4), ('opcode0', 7), ('s', 1), ('rd', 4), ('rn', 4), ('rs', 4), ('opcode1', 4), ('rm', 4)])
multiply.setVarField('rd', ('REGS', 0))
multiply.setVarField('rs', ('REGS', 0))
multiply.setVarField('rm', ('REGS', 0))
multiply.setBitfield('opcode1', [1, 0, 0, 1])

swi = trap.MachineCode([('cond', 4), ('one', 4), ('swi_number', 1)])

# Co-Processor Instructions
cp_ls = trap.MachineCode([('cond', 4), ('opcode', 3), ('p', 1), ('u', 1), ('n', 1), ('w', 1), ('l', 1), ('rn', 4), ('crd', 4), ('cpnum', 4), ('offset', 8)])
cp_ls.setBitfield('opcode', [1, 1, 0])
cp_ls.setVarField('rn', ('REGS', 0))
cp_dataProc = trap.MachineCode([('cond', 4), ('opcode0', 4), ('opcode1', 4), ('crn', 4), ('crd', 4), ('cpnum', 4), ('opcode2', 4), ('zero', 1), ('crm', 4)])
cp_dataProc.setBitfield('opcode0', [1, 1, 1, 0])
cp_regMove = trap.MachineCode([('cond', 4), ('opcode0', 4), ('opcode1', 3), ('l', 1), ('crn', 4), ('crd', 4), ('cpnum', 4), ('opcode2', 4), ('one', 1), ('crm', 4)])
cp_regMove.setBitfield('opcode0', [1, 1, 1, 0])
