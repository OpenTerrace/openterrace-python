    def select_fluid_schemes(self, diff=None, conv=None, coupling=False):
        """Imports the specified convection and diffusion schemes from the available schemes in schemes.py.
        """
        module = __import__('schemes')
        if conv:
            try:
                self.fluid.conv = getattr(module.Convection, conv)
            except:
                raise Exception('Valid convection schemes are: '+str([method for method in dir(module.Convection) if method.startswith('__') is False]))     
        else:
            self.fluid.conv = conv
        if diff:
            try:
                self.fluid.diff = getattr(module.Diffusion, diff)
            except:
                raise Exception('Valid diffusion schemes are: '+str([method for method in dir(module.Diffusion) if method.startswith('__') is False]))
        else:
            self.fluid.diff = diff
        self.fluid.coupling = coupling