# Jason Liang
# PCA.py

# Library imports
import numpy as np

# Function that calculates the covariance matrix
def compute_covariance_matrix(Z):
    
    # Uses numpy to calculate the covariance of Z
    covariance = np.cov(Z.T)

    return covariance

# Function that calculates the PCS from the covariance matrix
def find_pcs(cov):

    # Saves eigenvalues to L and eigenvectors to pcs
    (L, pcs) = np.linalg.eig(cov)

    # Create temp variables for moving eigenvalues and eigenvectors into largest to smallest
    tempL = L[0]
    tempPCS = pcs[0]

    # Sorts the index so it is now greatest to smallest
    # This will only work with 2D arrays      
    if(L[0] < L[1]):
        L[0] = L[1]
        L[1] = tempL

        pcs[0] = pcs[1]
        pcs[1] = tempPCS

    return pcs, L


# Projects the data onto a single axis
def project_data(Z, pcs, L):

    # Declaration of Z_star for manipulation
    Z_star = []

    # Grabs all the values from the first column
    data = pcs[:, 0]

    # Creates projection data and appends it to Z_star
    for i in Z:
        projection = np.dot(i, data)
        Z_star.append(projection)

    return Z_star