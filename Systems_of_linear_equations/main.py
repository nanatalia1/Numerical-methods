from math import sin
import time
from matplotlib import pyplot

class Matrix:
    def createMatrix(self, N, a1, a2, a3):
        matrix=[]
        for i in range(N):
            matrix_x=[] #rzedzy
            for j in range(N):
                if i==j:
                    matrix_x.append(a1)
                elif i - 1 <= j <= i + 1:
                    matrix_x.append(a2)
                elif i-2<= j <=i+2:
                    matrix_x.append(a3)
                else:
                    matrix_x.append(0)
            matrix.append(matrix_x)
        return matrix

    def add(self, A, B):
        sum_matrix=A
        for i in range(len(sum_matrix)):
            for j in range(len(sum_matrix[0])):
                sum_matrix[i][j]+=B[i][j]
        return sum_matrix

    def substract(self, A, B):
        sub_matrix=A
        for i in range(len(sub_matrix)):
            for j in range(len(sub_matrix[0])):
                sub_matrix[i][j]+=B[i][j]
        return sub_matrix

    def multiply(self, A, b):
        n = len(A[0])
        mul = Vector.createZerosVector(Vector, len(A))
        for i in range(len(A)):
            for j in range(n):
                mul[i] += A[i][j] * b[j]
        return mul

    def jacobi(self, a, B):
        start=time.time()
        A = a
        b = B
        x_old = Vector.createZerosVector(Vector, len(A[0]))
        x_new = Vector.createZerosVector(Vector, len(A[0]))
        it = 0
        r=[]
        iter=[]
        while (True):
            for i in range(len(A)):
                sigma = 0
                for j in range(len(A)):
                    if j != i:
                        sigma += A[i][j] * (x_old[j])
                x_new[i] = (b[i] - sigma) / A[i][i]
            x_old=x_new
            Mul = self.multiply(self, A, x_old)
            res = Vector.substract(Vector, Mul, b)
            r.append(Vector.norm(Vector, res))
            iter.append(it)
            if it==50:
                pyplot.plot(iter, r, label="LU", color="green")
                pyplot.ylabel('liczba iteracji')
                pyplot.xlabel('Wartość normy')
                pyplot.title('Zależność czasu od liczby niewiadomych')
                pyplot.show()
            if Vector.norm(Vector, res) < 10 ** (-9):
                break
            it += 1
        print('Jacobi - liczba iteracji: ', it)
        print('Jacobi - czas: ',time.time()-start)
        return time.time()-start
    def gauss_seidel(self, a, B):
        start = time.time()
        A=a
        b=B
        x=Vector.createZerosVector(Vector, len(A[0]))
        x_new=Vector.createZerosVector(Vector, len(A[0]))
        it=0
        while(True):
            for i in range(len(A)):
                sigma=0
                for j in range(len(A)):
                    if j < i:
                        sigma += A[i][j]*x_new[j]
                    if j > i:
                        sigma += A[i][j]*x[j]

                x_new[i]=(b[i]-sigma)/A[i][i]
            x=x_new

            Mul=self.multiply(self, A, x)

            res=Vector.substract(Vector, Mul, b)

            if Vector.norm(Vector, res) < 10**( -9):
                break
            else:
                it+=1
        print('Gauss-seidler - liczba iteracji: ', it)
        print('Gauss-seidler - czas: ', time.time() - start)
        x=[]
        for i in range(it):
            x.append(i)
        pyplot.plot(x, res, label="Gauss-Seidel: błąd", color="red")
        pyplot.ylabel('Czas (s)')
        pyplot.xlabel('Liczba niewiadomych')
        pyplot.title('Zależność czasu od liczby niewiadomych')
        pyplot.show()

        return time.time() - start

    def LU_factorization(self, A, b, A_c):

        L = Matrix.createMatrix(Matrix, len(A), 0, 0, 0)
        for i in range(len(A)):
            L[i][i] = 1
        U = A
        start = time.time()

        for j in range(len(A)):
            for i in range(j + 1):
                U[i][j] = A[i][j]
                for k in range(i):
                    U[i][j] -= L[i][k] * U[k][j]

            for i in range(j + 1, len(A)):
                for k in range(j):
                    L[i][j] -= L[i][k] * U[k][j]
                L[i][j] += A[i][j]
                L[i][j] /= U[j][j]

        #Ly = b forward substitution
        y = Vector.createZerosVector(Vector, len(A))
        for i in range(len(y)):
            y[i]= b[i]
            for j in range(i):
                y[i] -= (L[i][j] * y[j])
            y[i] = y[i] / L[i][i]

        # Ux = y backward substitution
        x = Vector.createZerosVector(Vector, len(A))
        for i in range(len(A) - 1, -1, -1):
            x[i] = y[i]
            for j in range(i + 1, len(A)):
                x[i] -= U[i][j] * x[j]
            x[i] = x[i] / U[i][i]


        Mul = Matrix.multiply(Matrix, A_c, x)
        res = Vector.substract(Vector, Mul, b)
        res = Vector.norm(Vector, res)
        print("Norma z residuum dla faktoryzacji LU wynosi: ", res)

        return (time.time() - start)
class Vector:
    def createVector(self, N):
        f=8
        vector=[]
        for n in range(N):
            vector.append(sin(n*(f+1)))
        return vector

    def createZerosVector(self, n):
        v=[]
        for i in range(n):
            v.append(0)
        return v



    def substract(self, A, b):
        sub_vector=A
        for i in range(len(A)):
            sub_vector[i]-=b[i]

        return sub_vector

    def norm(self, v):
        sum=0
        for i in v:
            sum+=i**2
        return sum ** 0.5

if __name__ == '_main_':
    e=8
    a1=5+e
    a2=-1
    a3=-1
    N=91
    #A------
    A=Matrix.createMatrix(Matrix, N, a1, a2, a3)
    b=Vector.createVector(Vector, N)

    #B-------
    #Matrix.jacobi(Matrix, A, b)
    #Matrix.gauss_seidel(Matrix, A, b)

    #C-------
    a1=3
    A_c = Matrix.createMatrix(Matrix, N, a1, a2, a3)
    A = Matrix.createMatrix(Matrix, N, a1, a2, a3)
    b_c = Vector.createVector(Vector, N)
    #Matrix.jacobi(Matrix, A_c, b_c)
    #Matrix.gauss_seidel(Matrix, A_c, b_c)

    #D-------
    Matrix.LU_factorization(Matrix, A, b, A_c)
    #E-------
    N = [100, 500, 1000, 2000, 3000]
    time_jacobi = []
    time_gs = []
    time_lu = []
    e = 8
    a1 = 5 + e
   # for n in N:
    #    A=Matrix.createMatrix(Matrix, n, a1, a2, a3)
     #   b=Vector.createVector(Vector, n)

      #  time_jacobi.append(Matrix.jacobi(Matrix, A, b))
      #  time_gs.append(Matrix.gauss_seidel(Matrix, A, b))
        #time_lu.append(Matrix.LU_factorization(A, b))

    #pyplot.plot(N, time_jacobi, label="Jacobi", color="red")
    #pyplot.plot(N, time_gs, label="Gauss-Seidl", color="blue")
   # pyplot.plot(N, time_lu, label="LU", color="green")

    #pyplot.ylabel('Czas (s)')
    #pyplot.xlabel('Liczba niewiadomych')
    #pyplot.title('Zależność czasu od liczby niewiadomych')
    #pyplot.show()
