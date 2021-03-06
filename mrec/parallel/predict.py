"""
Prediction task to run on an ipython engine.
"""

def run(task):

    # import modules required by engine
    import os
    import subprocess
    import numpy as np
    from scipy.sparse import coo_matrix

    from mrec import load_sparse_matrix, load_recommender
    from mrec.evaluation import Evaluator

    modelfile,input_format,trainfile,test_input_format,testfile,outdir,start,end,evaluator,generate = task

    # initialise the model
    model = load_recommender(modelfile)
    dataset = load_sparse_matrix(input_format,trainfile)

    outfile = os.path.join(outdir,'recs.{0}-{1}.tsv'.format(start,end))

    if generate:
        # generate recommendations for our batch of users
        out = open(outfile,'w')
        recs = model.range_recommend_items(dataset,start,end,max_items=20,return_scores=True)
        for u,items in zip(xrange(start,end),recs):
            for i,w in items:
                print >>out,'{0}\t{1}\t{2}'.format(u+1,i+1,w)  # write as 1-indexed
        out.close()

        # record success
        cmd = ['touch',os.path.join(outdir,'{0}-{1}.SUCCESS'.format(start,end))]
        subprocess.check_call(cmd)

    # load the test data
    testdata = load_sparse_matrix(test_input_format,testfile).tocsr()

    # return evaluation metrics
    return evaluator.process(testdata,outfile,start,end)
