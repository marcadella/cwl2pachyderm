# cwl2pachyderm

A [CWL](https://www.commonwl.org/) to [Pachyderm](https://github.com/pachyderm/pachyderm) converter aiming at 
converting a set of CWL workflow definitions into a set of Pachyderm pipeline definitions.
This would make possible to run CWL workflows on Kubernetes.

## Project state

This project is currently a draft destined to narrow down the design space.
The code is by no means usable and is not even likely to run.

## Requirements

Python 3.8 or later.

## Getting started

`python pachyderm_convertor.py ../testdata/md5sum.cwl ../testdata/md5sum.json`

This should generate a pachyderm definition file able to perform the same function as the cwl workflow provided as input.
For now only `CommandLineTool` have been considered.

## Design discussion

### Concepts mapping

#### Parameters

Pachyderm takes an approach where any runtime data is a file. This is to preserve data provenance.
For instance, it does not allow the passing of parameters at runtime: parameters has to be written in a file.
This does not map well with the richness of CWL data types.

One approach is therefore to introduce some logic in order to add one (or more) parameter file in a format of choice and add it to 
each pipeline's input (using `cross`). Before the tool is executed, the file needs to be parsed and the parameters have to be inserted in the command line starting the tool.  
Unfortunately this means that the docker image must have a shell installed.
In addition, a fair amount of logic has to be implemented/automatically generated before an after each tool in order to fall back to CWL output types instead of files.

Another approach is to start a new instance of pachyderm pipeline for each run and destroy it after the job has completed.
A way to achieve this would be to use random repo names.  
Following this approach means that each pipeline definition file has to be generated "just on time" with
the `cmd` field containing the runtime parameters. Once the file is generated the Pachyderm pipeline has to be started then destroyed upon completion of the job.
The fact that one need to take control over the pipelines instantiation removes most of the appeal to use such a pipeline orchestrator.
Therefore this approach does not seem promising.

#### Expressions and JS logic

Once again, Pachyderm being fairly static, it makes the support for CWL expressions and JavaScript logic awkward.
A container serving expression/JS logic evaluation may be considered.

#### Fields

Other than that, CWL definition fields map fairly well to Pachyderm fields.

#### Conclusion

It seems that the difference in philosophies between CWL and Pachyderm makes an implementation of a converter unfavorable.
It could be considered to support only a subsets of CWL but the practical use of the converter would then be very limited.

### About this implementation

Given the complexity of some of the CWL spec (command generation for instance), the idea was to inherit from `SingleJobExecutor` from the [CWL reference implementation](https://github.com/common-workflow-language/cwltool),
where the `run_jobs` method is overridden to convert the `Job` into a `Pipeline` object then print it.