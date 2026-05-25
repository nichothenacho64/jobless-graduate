export const DATA_DIR = "../data/processed/";

const REMOVED_MODE_BAR_BUTTONS = [
    "select2d", "lasso2d",
    "zoomIn2d", "zoomOut2d",
    "autoScale2d",
    "hoverCompareCartesian", "hoverClosestCartesian",
    "toggleSpikelines"
];

const TO_IMAGE_BUTTON_OPTIONS = { format: "png" };
const TRANSPARENT_BACKGROUND = "rgba(0, 0, 0, 0)";

export const CHART_1_ID = "chart_1_transition_window";
export const CHART_2_ID = "chart_2_subgroup_bottleneck";
export const CHART_3_ID = "chart_3_gap_shapes";
export const CHART_4_ID = "chart_4_field_conversion";
export const CHART_5_ID = "chart_5_work_fit";
export const CHART_6A_ID = "chart_6a_skill_by_age";
export const CHART_6B_ID = "chart_6b_degree_supply";
export const CHART_7_ID = "chart_7_subgroup_comparator";
export const CHART_METADATA_ID = "chart_metadata";

export const GLOBAL_TRACES = {
    hoverlabel: {
        align: "left",
        font: { size: 11 }
    },
    marker: {
        line: {
            width: 1.5
        }
    }
};

export const GLOBAL_LAYOUT = {
    paper_bgcolor: TRANSPARENT_BACKGROUND,
    plot_bgcolor: TRANSPARENT_BACKGROUND
};

export const GLOBAL_CONFIG = {
    responsive: true,
    displayModeBar: "hover",
    displaylogo: false,
    modeBarButtonsToRemove: REMOVED_MODE_BAR_BUTTONS,
    toImageButtonOptions: TO_IMAGE_BUTTON_OPTIONS
};

export const THEME_COLOURS = {
    amber700: "#A55A1f",
    blue700: "#2F5D7E",
    amber500: "#D08A3C",
    blue500: "#5E88A8",
    amber300: "#E7C48B",
    blue300: "#AFC6D8",
    grey500: "#a0a0a0",
    textColour: "#1F2328",
    backgroundColour: "#FFFDF9"
};

export const HOVERLABEL_BORDER_COLOURS = {
    [THEME_COLOURS.amber700]: THEME_COLOURS.amber500,
    [THEME_COLOURS.amber500]: THEME_COLOURS.amber300,
    [THEME_COLOURS.amber300]: THEME_COLOURS.amber700,
    [THEME_COLOURS.blue700]: THEME_COLOURS.blue500,
    [THEME_COLOURS.blue500]: THEME_COLOURS.blue300,
    [THEME_COLOURS.blue300]: THEME_COLOURS.blue700,
    "#FFF": THEME_COLOURS.amber500
};



export const CHART_1_TRACE_COLOURS = [
    THEME_COLOURS.amber500, 
    THEME_COLOURS.blue500, 
    THEME_COLOURS.amber700
];

export const CHART_6A_TRACE_COLOURS = [
    THEME_COLOURS.blue700,
    THEME_COLOURS.blue500,
    THEME_COLOURS.blue300,
    THEME_COLOURS.amber300,
    THEME_COLOURS.amber700
];

const DUMBBELL_BASE_HEIGHT = 60;
const DUMBBELL_ROW_HEIGHT = 60;

export const CHART_2_DIMENSIONS = {
    baseHeight: DUMBBELL_BASE_HEIGHT,
    rowHeight: DUMBBELL_ROW_HEIGHT,
    leftMargin: 220,
    rightMargin: 150,
};

export const CHART_3_DIMENSIONS = {
    baseHeight: DUMBBELL_BASE_HEIGHT,
    rowHeight: DUMBBELL_ROW_HEIGHT,
    leftMargin: 280,
    rightMargin: 20,
};

export const UNITS_TO_LABELS = {
    "percentage_point": " (pp)",
    "percent": " (%)"
};

export const CHART_AXES = {
    chart1XAxis: "Graduation year",
    chart1YAxis: "Full-time employment",
    chart2XAxis: "2024 short-term full-time employment (%)",
    chart3XAxis: "Signed full-time employment gap (percentage points)",
};

export const DUMBBELL_LINE = {
    width: 2.5,
    color: THEME_COLOURS.grey500
};

export const DIAGONAL_LINE = {
    color: THEME_COLOURS.textColour,
    width: 2,
    dash: "dash"
};

export const CHART_4_GAINS = {
    high: 25,
    medium: 15,
    low: 8,
};
