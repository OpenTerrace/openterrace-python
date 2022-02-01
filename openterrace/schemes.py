class Convective:
    def upwind(C, T):
        return (C[1:-1])*T[:-2] + (-C[1:-1])*T[1:-1]

    # def lax_wendroff(C, T): 
    #     return T[1:-1] - C/2*(T[2:]-T[:-2]) + C**2.0/2*(T[2:]-2*T[1:-1]+T[:-2])

class Diffusion:
    def central_difference(C, T):
        return (C[1:-1])* (T[:-2] - 2*T[1:-1] + T[2:])