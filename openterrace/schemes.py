class Convection:
    """Various schemes for discretising the convection term.
    """
    def upwind(C, T):
        """First-order accurate upwind scheme.
        """
        return (-C[1:-1])*T[:-2] + (C[1:-1])*T[1:-1]

    # def lax_wendroff(C, T): 


class Diffusion:
    """Various schemes for discretising the diffusion term.
    """
    def central_difference(C, T):
        """Second-order accurate central diffence scheme.
        """
        return (C[1:-1])* (T[:-2] - 2*T[1:-1] + T[2:])