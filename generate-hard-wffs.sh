#!/bin/bash -x

# Copyright (c) 2018, Henry Kautz <henry.kautz@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 2
# of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

# use:

if (( $# != 3 )); then
    echo "generate-hard-wffs.sh number_vars start_wff_numer end_wff_number"
    exit
fi

v=$1
s=$2
e=$3

(( r = 425 ))
(( c = ( v * r ) / 100 ))
for x in $(seq -f "%03g" $s $e)
do
   echo "./makewff -cnf 3 $v $c > f$v-r$r-x$x.cnf"
done


