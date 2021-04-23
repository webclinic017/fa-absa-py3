from __future__ import print_function
"""----------------------------------------------------------------------------
MODULE
    FSingularValueDecomposition - Module containing singular value 
    decomposition factorization and backsubstitution

DESCRIPTION
    This Python implementation replicates the built-in FRONT ARENA 
    singular value decomposition, i.e. the algorithms in Numerical 
    Recipes In C chapter 2.6
    
    (c) Copyright 2011 by SunGard Front Arena. All rights reserved.

----------------------------------------------------------------------------"""

import math

def svdsolve(u, w, v, m, n, b, x, tmp = None, zero = 1.e-12):
    """
    The function svdsolve solves the linear equations system 
        U W V^T x = b
    where U, W, V^T are the singulare value decomposition of
    the original M x N matrix A
    
    svdsolve( u, w, v, m, n, b, x, tmp = None, zero = 1.e-12 )

    Input arguments
        u               svd M x N column-orthogonal matrix
        w               svd N x N diagonal matrix with singular values
        v               svd N x N orthogonal matrix (not transpose)
        m               number of rows in matrix A
        n               number of columns in matrix A
        b               RHS vector of A x = b, arrray of size M
        x               unknown solution vector to be solved, array of size N
        tmp             work area, array of size n
        zero            zero, small value

    Description
        Solves the equation U W V^T x = b for x, where 
        U, W, V^T are the singulare value decomposition of
        the original M x N matrix A

    Reference
        This routine is based on the C routine svbksb 
        of Numerical Recipes In C, chapter 2-6.
    """
    if not tmp:
        tmp = [0.0] * n
    # Calculate U^T B and divide by w_j
    for j in range(n):
        s = 0.0
        # Nonzero result only if w_j is nonzero
        if abs(w[j]) > zero:
            for i in range(m):
                s += ( u[i][j] * b[i] )
            s = s / w[j]
        tmp[j] = s
    # Matrix multiply by V to get answer
    for i in range(n):
        s = 0
        for j in range(n):
            s += v[i][j] * tmp[j]
        x[i] = s


def svdcmp( a, m, n, w, v, rv1):
    """
    The function svdcmp factorize the matrix A into a singular value 
    decomposition, i.e. U W V^T = A.
    
    svdcmp(a, m, n, w, v, rv1 )

    Input arguments
        a               matrix (M x N) to be factored, overwritten with u
        m               number of rows in matrix A
        n               number of columns in matrix A
        w               svd N x N diagonal matrix with singular values
        v               svd N x N orthogonal matrix (not transpose)
        tmp             work area, array of size n

    Description
        Factorize a M x N matrix, A, into a singulare value decomposition
        where U W V^T = A. Matrix A is overwritten with the orthogonal 
        matrix M x N matrix U. The diagonal matrix W is output as a 
        vector w of length n. The orthogonal N x N matrix V (not the 
        transpose V^T) is output.

    Reference
        This routine is based on the C routine svdcmp 
        of Numerical Recipes In C, chapter 2-6.
    """
    flag=0
    g = scale = anorm = 0.0
    if m < n:
        print ("ML_SVDCMP: You must augment A with extra zero rows")
        return 0
    for i in range(n):
        l = i+1;
        rv1[i] = scale * g
        g = s = scale = 0.0
        if i < m:
            for k in range(i, m):
                scale += abs( a[k][i] )
            if scale:
                for k in range(i, m):
                    a[k][i] = a[k][i] / scale
                    s += a[k][i] * a[k][i]
                f = a[i][i];
                g = -SIGN( math.sqrt(s), f )
                h = f * g - s
                a[i][i] = f - g
                if i != n-1:
                    for j in range(l, n):
                        s = 0.0
                        for k in range(i, m):
                            s += a[k][i] * a[k][j]
                        f = s / h
                        for k in range(i, m):
                            a[k][j] += f * a[k][i]
                for k in range(i, m):
                    a[k][i] *= scale
        w[i] = scale * g
        g = s = scale = 0.0
        if i < m and i != n-1:
            for k in range(l, n):
                scale += abs( a[i][k] )
            if scale:
                for k in range(l, n):
                    a[i][k] = a[i][k] / scale
                    s += a[i][k] * a[i][k]
                f = a[i][l]
                g = -SIGN( math.sqrt(s), f )
                h = f * g - s
                a[i][l] = f - g
                for k in range(l, n):
                    rv1[k] = a[i][k] / h
                if i != m-1:
                    for j in range(l, m):
                        s = 0.0
                        for k in range(l, n):
                            s += a[j][k] * a[i][k]
                        for k in range(l, n):
                            a[j][k] += s * rv1[k]
                for k in range(l, n):
                    a[i][k] *= scale
        anorm = max( anorm, ( abs( w[i] ) + abs( rv1[i] ) ) )
    for i in reversed( list(range(n)) ):
        if i < n-1:
            if g:
                for j in range(l, n):
                    v[j][i] = ( a[i][j] / a[i][l] ) / g
                for j in range(l, n):
                    s = 0.0
                    for k in range(l, n):
                        s += a[i][k] * v[k][j]
                    for k in range(l, n):
                        v[k][j] += s * v[k][i]
            for j in range(l, n):
                v[i][j] = v[j][i] = 0.0
        v[i][i]=1.0;
        g = rv1[i]
        l = i
    for i in reversed( list(range(n)) ):
        l = i + 1
        g = w[i]
        if i < n:
            for j in range(l, n):
                a[i][j] = 0.0
        if g:
            g = 1.0 / g
            if i != n-1:
                for j in range(l, n):
                    s = 0.0
                    for k in range(l, m):
                        s += a[k][i] * a[k][j]
                    f = ( s / a[i][i] ) * g
                    for k in range(i, m):
                        a[k][j] += f * a[k][i]
            for j in range(i, m):
                a[j][i] = a[j][i] * g
        else:
            for j in range(i, m):
                a[j][i] = 0.0
        a[i][i] += 1
    for k in reversed( list(range(n)) ):
        for its in range(30):
            flag = 1
            for l in range(k,-1,-1): # reversed( range(k) ):
                nm = l-1
                if abs( rv1[l] ) + anorm == anorm:
                    flag = 0
                    break;
                if abs( w[nm] ) + anorm == anorm: 
                    break;
            if flag:
                c = 0.0
                s = 1.0
                for i in range(l, k):
                    f = s * rv1[i]
                    if abs(f) + anorm != anorm:
                        g = w[i]
                        h = PYTHAG(f, g)
                        w[i] = h
                        h =1.0 / h
                        c =g * h
                        s = (-f * h)
                        for j in range(m):
                            y = a[j][nm]
                            z = a[j][i]
                            a[j][nm] = y * c + z * s
                            a[j][i] = z * c - y * s
            z = w[k]
            if l == k:
                if z < 0.0:
                    w[k] = -z
                    for j in range(n): 
                        v[j][k] = (-v[j][k])
                break;
            if its == 30:
                print ("No convergence in 30 ML_SVDCMP iterations")
                return 0
            x = w[l]
            nm = k-1
            y = w[nm]
            g = rv1[nm]
            h = rv1[k]
            f = ( (y - z) * (y + z) + (g - h) * (g + h) ) / ( 2.0 * h * y )
            g = PYTHAG(f, 1.0 )
            f = ( (x - z) * (x + z) + h * ( (y / (f + SIGN(g, f) ) ) - h) ) / x
            c = s = 1.0
            for j in range(l, nm+1):
                i = j+1
                g = rv1[i]
                y = w[i]
                h = s * g
                g = c * g
                z = PYTHAG(f, h)
                rv1[j] = z
                c = f / z
                s = h / z
                f = x * c + g * s
                g = g * c - x * s
                h = y * s
                y = y * c
                for jj in range(n):
                    x = v[jj][j]
                    z = v[jj][i]
                    v[jj][j] = x * c + z * s
                    v[jj][i] = z * c - x * s
                z = PYTHAG(f, h)
                w[j] = z
                if z:
                    z = 1.0 / z
                    c = f * z
                    s = h * z
                f = (c * g) + (s * y)
                x = (c * y) - (s * g)
                for jj in range(m):
                    y = a[jj][j]
                    z = a[jj][i]
                    a[jj][j] = y * c + z * s
                    a[jj][i] = z * c - y * s
            rv1[l] = 0.0
            rv1[k] = f
            w[k] = x
    return 1;

    
def PYTHAG(a,b):
    at = abs(a)
    bt = abs(b)
    if at > bt:
        ct = bt / at
        return at * math.sqrt( 1.0 + ct * ct )
    else:
        if bt:
            ct = at / bt
            return bt * math.sqrt( 1.0 + ct * ct )
        else:
            return 0.0
            
            
def SIGN(a, b):
    if b >= 0.0:
        return abs(a)
    else: 
        return -abs(a)

