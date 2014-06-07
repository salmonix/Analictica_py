def compose(*args):
    """The input list is as [ module, parameter ]. Returns a list of initialized modules."""
    
    for i in args:
        obj=None
        try:
            mod = i[0]
            import i[0]    # this will not work, but I sould find out why
            obj=i[0](i[1])
        raise:
        