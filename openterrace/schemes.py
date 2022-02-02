class Convective():
    """Various schemes for discretising the convective term.
    """
    def upwind(C, T):
        """First-order accurate upwind scheme.
        """
        return (C[1:-1])*T[:-2] + (-C[1:-1])*T[1:-1]

        # def lax_wendroff(C, T): 
        #     return T[1:-1] - C/2*(T[2:]-T[:-2]) + C**2.0/2*(T[2:]-2*T[1:-1]+T[:-2])

class Diffusion():
    """Various schemes for discretising the diffusive term.
    """
    def central_difference(C, T):
        """Second-order accurate central diffence scheme.
        """
        return (C[1:-1])* (T[:-2] - 2*T[1:-1] + T[2:])