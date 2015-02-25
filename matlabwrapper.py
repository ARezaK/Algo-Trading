import matlab_wrapper

mat = matlab_wrapper.MatlabSession()

mat.eval("load cities")

categories = mat.get('categories')
ratings = mat.workspace.ratings

print ratings


