class TestFunctions():

    def analytical_1d_diffusion(self, t_end=None, h=None, r=None, k=None, rho=None, cp=None, n_terms=5):
        def func(lambda_n):
            Bi = h*r/k
            return 1-lambda_n*np.cos(lambda_n)/np.sin(lambda_n)-Bi
            
            Fo = k/(rho*cp) * t_end / r**2

            arr_lambda_n = np.array([])
            i = 0.1
            while len(arr_lambda_n) < n_terms:
                lambda_n = float("%0.6f" % least_squares(func, i, bounds = (0.1, np.inf)).x)

                if lambda_n not in arr_lambda_n:
                    arr_lambda_n = np.append(arr_lambda_n ,lambda_n)
                i += 0.01

            theta = []
            for _r in self.r:
                theta = np.append(theta, (np.sum(4*(np.sin(arr_lambda_n)-arr_lambda_n*np.cos(arr_lambda_n))/(2*arr_lambda_n-np.sin(2*arr_lambda_n)) * np.exp(-arr_lambda_n**2*Fo) * np.sin(arr_lambda_n*_r/r)/(arr_lambda_n*_r/r))))
        return theta