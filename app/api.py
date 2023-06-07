from app.pipeline_i import Pipeline_I
from app.pipeline_ii import Pipeline_II
from app.utils.api_classes import Pipeline_i_data, Pipeline_ii_data, ScrapeData, FirstPassBaltimoreFilter, FirstPassTaxonFilter, SecondPass, FastaToGb, VmrFilter, CombineGenomeSegs, E2e_data
from app.utils.scrape_vmr import scrape, first_pass_taxon_filter, first_pass_baltimore_filter, second_pass, vmr_filter
from app.utils.process_fasta import fasta_to_genbank, combine_segments
from app.utils.end_to_end_entrypoint import split_payloads_for_e2e

from fastapi import FastAPI, BackgroundTasks
from fastapi.encoders import jsonable_encoder

description = """
    Genome Relationships Applied to Virus Taxonomy is a software framework for identifying and classifying viruses, based on analysis of entire genomes.
"""

tags_metadata = [
    {
        "name": "End to end",
        "description": "Run an end-to-end job using two passes across both pipelines",
    },
    {
        "name": "Pipeline I",
        "description": "PL1 description & user info",
    },
    {
        "name": "Pipeline II",
        "description": "PL2 description & user info.",
    },
    {
        "name": "VMR Utilities",
        "description": "Refresh Virus Metadata Resource (VMR) from ICTV and construct datasets."
    },
    {
        "name": "Automated Workflows",
        "description": "Pre-made workflows to automate the transition between a first pass PL2 run to a second pass PL1-2 run."
    },
]

app = FastAPI(
    title="GRAViTy V2",
    version="1.0",
    description=description,
    contact={
        "name": "Mayne Bio Analytics Ltd",
        "url": "http://www.mayneba.com",
        "email": "director@mayneba.com"
    },
    # RM < Check this license is appropriate
    license_info={
        "name": "Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)",
        "url": "https://creativecommons.org/licenses/by-nc/4.0/",
    },
    openapi_tags=tags_metadata
)


'''Dev Endpoints'''


@app.get("/", tags=["Dev Utilities"])
async def read_root():
    return {"response": "API is healthy. Append the current URL to include '/docs/' at the end to visit the GUI."}

'''Unified Endpoints'''

@app.post("/end_to_end/", tags=["End to end"])
async def end_to_end(payload: E2e_data, background_tasks: BackgroundTasks):
    payload = jsonable_encoder(payload)
    background_tasks.add_task(run_end_to_end, payload)
    return "Task fired successfully, running in background"

def run_end_to_end(payload):
    payload_fp_pl1, payload_fp_pl2, payload_sp_pl1, payload_sp_pl2 = split_payloads_for_e2e(payload)
    run_pipeline_i_full(payload_fp_pl1)
    run_pipeline_ii_full(payload_fp_pl2)
    run_pipeline_i_full(payload_sp_pl1)
    run_pipeline_ii_full(payload_sp_pl2)


'''PL1 Entrypoints'''


@app.post("/pipeline_i_full/", tags=["Pipeline I"])
async def pipeline_i_full(payload: Pipeline_i_data, background_tasks: BackgroundTasks):
    payload = jsonable_encoder(payload)
    background_tasks.add_task(run_pipeline_i_full, payload)
    return "Task fired successfully, running in background"


def run_pipeline_i_full(payload):
    pl = Pipeline_I(payload)
    pl.read_genome_desc_table()


@app.post("/pipeline_i_from_pphmmdb_construction/", tags=["Pipeline I"])
async def pipeline_i__from_pphmmdb_construction(payload: Pipeline_i_data, background_tasks: BackgroundTasks):
    payload = jsonable_encoder(payload)
    background_tasks.add_task(
        run_pipeline_i_from_pphmmdb_construction, payload)
    return "Task fired successfully, running in background"


def run_pipeline_i_from_pphmmdb_construction(payload):
    pl = Pipeline_I(payload)
    pl.pphmmdb_construction()


@app.post("/pipeline_i_from_ref_virus_annotator/", tags=["Pipeline I"])
async def pipeline_i__from_ref_virus_annotator(payload: Pipeline_i_data, background_tasks: BackgroundTasks):
    payload = jsonable_encoder(payload)
    background_tasks.add_task(run_pipeline_i_from_ref_virus_annotator, payload)
    return "Task fired successfully, running in background"


def run_pipeline_i_from_ref_virus_annotator(payload):
    pl = Pipeline_I(payload)
    pl.ref_virus_annotator()


@app.post("/pipeline_i_from_graph_generator/", tags=["Pipeline I"])
async def pipeline_i__from_graph_generator(payload: Pipeline_i_data, background_tasks: BackgroundTasks):
    payload = jsonable_encoder(payload)
    background_tasks.add_task(run_pipeline_i_from_graph_generator, payload)
    return "Task fired successfully, running in background"


def run_pipeline_i_from_graph_generator(payload):
    pl = Pipeline_I(payload)
    pl.make_graphs()


@app.post("/pipeline_i_from_mutual_info_calculator/", tags=["Pipeline I"])
async def pipeline_i_from_mutual_info_calculator(payload: Pipeline_i_data, background_tasks: BackgroundTasks):
    payload = jsonable_encoder(payload)
    background_tasks.add_task(
        run_pipeline_i_from_mutual_info_calculator, payload)
    return "Task fired successfully, running in background"


def run_pipeline_i_from_mutual_info_calculator(payload):
    pl = Pipeline_I(payload)
    pl.mutual_info_calculator()


'''PL2 entrypoints'''


@app.post("/pipeline_ii_full/", tags=["Pipeline II"])
async def pipeline_ii_full(payload: Pipeline_ii_data, background_tasks: BackgroundTasks):
    payload = jsonable_encoder(payload)
    background_tasks.add_task(run_pipeline_ii_full, payload)
    return "Task fired successfully, running in background"


def run_pipeline_ii_full(payload):
    pl = Pipeline_II(payload)
    pl.read_genome_desc_table()


@app.post("/pipeline_ii_from_pphmmdb_construction/", tags=["Pipeline II"])
async def pipeline_ii_from_pphmmdb_construction(payload: Pipeline_ii_data, background_tasks: BackgroundTasks):
    payload = jsonable_encoder(payload)
    background_tasks.add_task(
        run_pipeline_ii_from_pphmmdb_construction, payload)
    return "Task fired successfully, running in background"


def run_pipeline_ii_from_pphmmdb_construction(payload):
    pl = Pipeline_II(payload)
    pl.pphmmdb_construction()


@app.post("/pipeline_ii_from_ucf_virus_annotator/", tags=["Pipeline II"])
async def pipeline_ii_from_ucf_virus_annotator(payload: Pipeline_ii_data, background_tasks: BackgroundTasks):
    payload = jsonable_encoder(payload)
    background_tasks.add_task(
        run_pipeline_ii_from_ucf_virus_annotator, payload)
    return "Task fired successfully, running in background"


def run_pipeline_ii_from_ucf_virus_annotator(payload):
    pl = Pipeline_II(payload)
    pl.ucf_virus_annotator()


@app.post("/pipeline_ii_from_virus_classification/", tags=["Pipeline II"])
async def pipeline_ii_from_virus_classification(payload: Pipeline_ii_data, background_tasks: BackgroundTasks):
    payload = jsonable_encoder(payload)
    background_tasks.add_task(
        run_pipeline_ii_from_virus_classification, payload)
    return "Task fired successfully, running in background"


def run_pipeline_ii_from_virus_classification(payload):
    pl = Pipeline_II(payload)
    pl.virus_classification()


'''Utility entrypoints'''


@app.post("/scrape_vmr/", tags=["VMR Utilities"])
async def run_vmr_scrape(trigger: ScrapeData):
    payload = jsonable_encoder(trigger)
    return scrape(payload)


@app.post("/construct_first_pass_vmr_baltimore_filter/", tags=["VMR Utilities"])
async def vmr_first_pass_baltimore_filter(trigger: FirstPassBaltimoreFilter):
    payload = jsonable_encoder(trigger)
    return first_pass_baltimore_filter(payload)

@app.post("/construct_first_pass_vmr_taxon_filter/", tags=["VMR Utilities"])
async def vmr_first_pass_taxon_filter(trigger: FirstPassTaxonFilter):
    payload = jsonable_encoder(trigger)
    return first_pass_taxon_filter(payload)

@app.post("/construct_second_pass_vmr/", tags=["VMR Utilities"])
async def vmr_second_pass(trigger: SecondPass):
    payload = jsonable_encoder(trigger)
    return second_pass(payload)

@app.post("/filter_vmr/", tags=["VMR Utilities"])
async def filter_that_vmr(trigger: VmrFilter):
    payload = jsonable_encoder(trigger)
    return vmr_filter(payload)

@app.post("/convert_fasta_to_genbank_and_vmr/", tags=["VMR Utilities"])
async def convert_fasta_to_genbank(trigger: FastaToGb):
    payload = jsonable_encoder(trigger)
    return fasta_to_genbank(payload)

@app.post("/combine_genome_segments/", tags=["VMR Utilities"])
async def convert_genome_segments(trigger: CombineGenomeSegs):
    payload = jsonable_encoder(trigger)
    return combine_segments(payload)
