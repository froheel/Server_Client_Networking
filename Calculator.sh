#!/bin/bash
val1=0
val2=0
operator=a
while :
do
echo
echo
echo
echo "press ctrl + z to exit"
echo
echo
echo

    while :
    do

        echo "Input the first value between 1 and 100"
        read val1
        if ! [[ "$val1" =~ ^[0-9]+$ ]]
        then
            echo "Alpha numaric input not allowed"
        else
            if [[ $val1 -gt 0 && $val1 -lt 101 ]];
            then
                break
            else
                echo "input out of range"
            fi
        fi

    done
    let valid=false 

    while :
    do

        echo "Input the second value between 1 and 100"
        read val2
        if ! [[ "$val2" =~ ^[0-9]+$ ]]
        then
            echo "Alpha numaric input not allowed"
        else
            if [[ $val2 -gt 0 && $val2 -lt 101 ]];
            then
                break
            else
                echo "input out of range"
            fi
        fi

    done
    while :
    do
        echo "Input the operatoin you want to perform a, s, d, m"
        read input
        operator=${input,,}
        case $operator in

        a)
            echo "adding $val1 and $val2 results in"
            ((val1 = val1 + val2))
            echo $val1
            break
            ;;

        s)
            echo "subtracting $val1 and $val2 results in"
            ((val1 = val1 - val2))
            echo $val1
            break
            ;;
        m)
            echo "multiplying $val1 and $val2 results in"
            ((val1 = val1 * val2))
            echo $val1
            break
            ;;
        d)
            echo "dividing $val1 and $val2 results in"
            ((val1 = val1 / val2))
            echo $val1
            break
            ;;
        *)
            echo "invalid operator"
            ;;
        esac 
    done
done
