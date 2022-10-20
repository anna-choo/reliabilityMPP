class GLOBAL():
    def __init__(self):
        print("hello")
        # folder dir
        self.dir = r'Z:\RehabData\Reliability Test\post-training'
        # the layer after date folder
        self.secondLayer_dir = "Labelled"

        # Global variable for metafile
        self.task_list = { "unilateral" : ["key_stand", "back", "mouth", "head", "grasp", "lateral", "towel"],
                            "bilateral" : ["step_down", "step_up", "kerb", "balance", "tug", "10m", "static", "balance_static"],
                            "ignore_task" : ["key_sit", "static_norm", "lateral_cube", "step", "bb"]}
        self.mega_metafile = "ABILITYDATA_mega_metafile.xlsx"
        self.MEGA_METAFILE_DIR = r"Z:\RehabData\Process\Meta_Files"
        self.metafile_path = r"Z:\RehabData\Process\Meta_Files"
        self.number_filler = 3