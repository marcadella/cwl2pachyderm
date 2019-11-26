#!/usr/bin/env python3
import sys
import cwl_utils.parser_v1_0 as cwl
import cwl_utils.pachyderm.pachyderm_pipeline as pach
import jsonpickle
from ruamel import yaml
from cwltool import (executors, process, main as cwlmain, job as cwljob, docker)


class ParserExecutor(executors.SingleJobExecutor):
    def run_jobs(self,
                 process: process.Process,
                 job_order_object,  # type: Dict[Text, Any]
                 logger,            # type: logging.Logger
                 runtime_context    # type: RuntimeContext
                 ):  # type: (...) -> None

        jobiter = process.job(job_order_object, self.output_callback,
                              runtime_context)
        for job in jobiter:
            if job is not None: #cwltool.workflow.WorkflowJob or cwltool.docker.DockerCommandLineJob
                if isinstance(job, docker.DockerCommandLineJob):
                    convert_job(process, job)
            else:
                return #just because jobiter seems to get stuck with None
                #yaml.round_trip_dump(cwl.save(job), sys.stdout)


def main(*args, **kwargs):
    cwlmain.main(*args, **dict(kwargs, executor=ParserExecutor()))


def convert_job(process, job: docker.DockerCommandLineJob):
    docker_requirement: cwl.DockerRequirement = None
    resource_requirement: cwl.ResourceRequirement = None
    #Process missing 'id' and 'loadingOptions'
    #for req in job.hints:
    #    if req['class'] == "DockerRequirement":
    #        docker_requirement = cwl.load_field(req, cwl.DockerRequirementLoader,
    #                             process.id, process.loadingOptions)
    #    if req['class'] == "ResourceRequirement":
    #        resource_requirement = cwl.load_field(req, cwl.ResourceRequirementLoader,
    #                                            process.id, process.loadingOptions)
    for req in job.requirements:
        #yaml.round_trip_dump(cwl.save(req), sys.stdout)
        if isinstance(req, cwl.DockerRequirement):
            docker_requirement = req
        if isinstance(req, cwl.ResourceRequirement):
            resource_requirement = req
    if docker_requirement: #Not else here!
        resource_requests: cwl.ResourceRequests = pach.ResourceRequests()
        resource_limits: cwl.ResourceLimits = pach.ResourceLimits()
        if resource_requirement:
            resource_requests = pach.ResourceRequests(memory=resource_requirement.ramMin,
                                                     cpu=resource_requirement.coresMin,
                                                     disk=resource_requirement.outdirMin)# + resource_requirement.tmpdirMin)
            resource_limits = pach.ResourceLimits(memory=resource_requirement.ramMax,
                                                 cpu=resource_requirement.coresMax,
                                                 disk=resource_requirement.outdirMax)# + resource_requirement.tmpdirMax)
        pdef = pach.PipelineDef(
                pipeline=pach.Pipeline(job.id),
                description="%s\n%s"%(job.label,job.doc),
                transform=pach.Transform(image=docker_requirement.dockerPull,
                                         cmd=job.command_line
                ),
            resource_requests=resource_requests,
            resource_limits=resource_limits,
        )
        print(pdef.toJson())
        return pdef
    else:
        print("Ignored since no DockerRequirement/Hint in %s"%job.name)
        return None


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
