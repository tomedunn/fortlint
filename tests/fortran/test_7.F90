        MODULE mod_a

          implicit none

          CALL sub_a1(w,a)
          CALL sub_b1(w,w,a)
          f = func_a2(a)

        contains

                ! ..............................
                function    func_a1(a)
                IMPLICIT NONE
                   INTEGER :: a
                   ! LOCAL

                   call sub_a1(w,a)
                   RETURN
                END function func_a1
                ! ..............................


                ! ..............................
                SUBROUTINE    sub_a1(xx,ii)
                IMPLICIT NONE
                   REAL :: xx
                   INTEGER :: ii

                   ii = xx
                   call sub_a1(xx,xx,ii)
                   func_a1(xx)

                   RETURN
                END SUBROUTINE sub_a1
                ! ..............................

                ! ..............................
                function    func_a2(a)
                IMPLICIT NONE
                   INTEGER :: a
                   ! LOCAL

                   call sub_inner(xx,xx,ii)
                   func_inner(xx)

                   CONTAINS
                      ! ..............................
                      function    func_inner(alpha)
                      IMPLICIT NONE
                         INTEGER :: alpha
                         ! LOCAL

                         call sub_a2(xx,xx,ii)
                         RETURN
                      END function func_inner
                      ! ..............................

                      ! ..............................
                      SUBROUTINE   sub_inner(xx,ii)
                      IMPLICIT NONE
                         REAL :: xx
                         INTEGER :: ii
                     
                         ii = xx
                         func_a1(xx)
                     
                         RETURN
                      END SUBROUTINE sub_inner
                      ! ..............................


                   RETURN
                END function func_a2
                ! ..............................

                ! ..............................
        end MODULE mod_a


        MODULE mod_b

          implicit none

        contains
                ! ..............................
                SUBROUTINE    sub_b1(x,y,i)
                IMPLICIT NONE
                   REAL :: x
                   REAL :: y 
                   INTEGER :: i
                   INTEGER :: j 
                   INTEGER :: li_ii

                   i = i + j
                   x = x + y
                   i = x
                   func_a2(x)

                   RETURN
                END SUBROUTINE sub_b1
                ! ..............................

                ! ..............................
                SUBROUTINE    sub_b2(i)
                IMPLICIT NONE
                   INTEGER :: i

                   func_b1(a)

                   RETURN
                END SUBROUTINE sub_b2
                ! ..............................

                ! ..............................
                function    func_b1(a,b,w)
                IMPLICIT NONE
                   INTEGER :: a
                   INTEGER :: b 
                   REAL :: w
                   ! LOCAL

                   call sub_b1(w,w,a)
                   RETURN
                END function func_b1 
                ! ..............................

                ! ..............................
        end MODULE mod_b

