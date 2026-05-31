export const DATA_DIR = "data/processed/";


// chart IDs
export const CHART_1A_ID = "chart_1a_degree_supply";
export const CHART_1B_ID = "chart_1b_skill_by_age";
export const CHART_2_ID = "chart_2_transition_window";
export const CHART_3_ID = "chart_3_subgroup_bottleneck";
export const CHART_4_ID = "chart_4_gap_shapes";
export const CHART_5_ID = "chart_5_field_conversion";
export const CHART_6_ID = "chart_6_work_fit";
export const CHART_7_ID = "chart_7_subgroup_comparator";
export const CHART_METADATA_ID = "chart_metadata";

export const CHART_TITLES = {
    chart1a: "More Australians now hold degrees",
    chart1b: "High-skill work is age-sorted",
    chart2: "The first year is the weak point",
    chart3: "The bottleneck is uneven",
    chart4: "Some gaps close while others persist",
    chart5: "Some fields recover after the first graduate year",
    chart6: "More work does not always mean better fit",
    chart7: "Inspect one subgroup gap"
};


// theme 

// export const FONT_FAMILY = "sans-serif"; // ! only for photo saving
export const FONT_FAMILY = '"Source Sans 3", sans-serif';

export const THEME_COLOURS = {
    amber700: "#A55A1f",
    blue700: "#2F5D7E",
    amber500: "#D08A3C",
    blue500: "#5E88A8",
    amber300: "#E7C48B",
    blue300: "#AFC6D8",
    grey500: "#a0a0a0",
    text: "#1F2328",
    background: "#FFFDF9"
};

export const HOVERLABEL_BORDER_COLOURS = {
    [THEME_COLOURS.amber700]: THEME_COLOURS.amber500,
    [THEME_COLOURS.amber500]: THEME_COLOURS.amber300,
    [THEME_COLOURS.amber300]: THEME_COLOURS.amber700,
    [THEME_COLOURS.blue700]: THEME_COLOURS.blue500,
    [THEME_COLOURS.blue500]: THEME_COLOURS.blue300,
    [THEME_COLOURS.blue300]: THEME_COLOURS.blue700,
    [THEME_COLOURS.background]: THEME_COLOURS.amber500
};

// global Plotly settings
const TRANSPARENT_BACKGROUND = THEME_COLOURS.text + "00";
const TO_IMAGE_BUTTON_OPTIONS = { format: "png" };
const REMOVED_MODE_BAR_BUTTONS = [
    "select2d", "lasso2d",
    "zoomIn2d", "zoomOut2d",
    "autoScale2d",
    "hoverCompareCartesian", "hoverClosestCartesian",
    "toggleSpikelines"
];

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

export const GLOBAL_TRACES = {
    hoverlabel: {
        align: "left",
        font: { size: 11 }
    },
    marker: { line: { width: 1.5 } }
};


// shared chart labels
export const UNITS_TO_LABELS = {
    "percentage_point": " (pp)",
    "percent": " (%)",
    "people": " (people)"
};


// shared chart styling
export const MARKER_SIZE = {
    small: 8,
    large: 10
};

export const DUMBBELL_LINE = {
    width: 2.5,
    color: THEME_COLOURS.grey500
};

export const DIAGONAL_LINE = {
    color: THEME_COLOURS.text,
    width: 2,
    dash: "dash"
};


// chart 1b
export const CHART_1B_TRACE_COLOURS = [
    THEME_COLOURS.blue700,
    THEME_COLOURS.blue500,
    THEME_COLOURS.blue300,
    THEME_COLOURS.amber300,
    THEME_COLOURS.amber700
];


// chart 2
export const CHART_2_TRACE_COLOURS = [
    THEME_COLOURS.amber500, 
    THEME_COLOURS.blue500, 
    THEME_COLOURS.amber700
];


// chart 3 and chart 4
const DUMBBELL_BASE_HEIGHT = 60;
const DUMBBELL_ROW_HEIGHT = 60;

export const CHART_3_DIMENSIONS = {
    baseHeight: DUMBBELL_BASE_HEIGHT,
    rowHeight: DUMBBELL_ROW_HEIGHT,
    leftMargin: 220,
    rightMargin: 150,
};

export const CHART_4_DIMENSIONS = {
    baseHeight: DUMBBELL_BASE_HEIGHT,
    rowHeight: DUMBBELL_ROW_HEIGHT,
    leftMargin: 280,
    rightMargin: 20,
};


// chart 5
export const CHART_5_GAIN_VALUES = {
    high: 25,
    medium: 15,
    low: 8,
};


// chart 7
export const CHART_7_RENDERING = {
    elementIds: {
        dropdownButton: "chart7DropdownButton",
        dropdownMenu: "chart7DropdownMenu",
        selectorLabel: "chart7SelectorLabel",
        explanationCard: "chart7ExplanationCard"
    },
    dimensions: {
        height: 360,
        leftMargin: 70,
        rightMargin: 20,
        topMargin: 60,
        bottomMargin: 50
    },
    yAxisPadding: {
        lower: 4,
        upper: 1
    }
};

export const CHART_7_VALUES = {
    gapPatternThresholds: {
        nearZero: 1,
        meaningful: 3,
        substantialShrinkRatio: 0.5
    },
    gapPatterns: {
        persists: {
            label: "Persists",
            colour: THEME_COLOURS.amber700,
            sentence: "This gap persists into the medium term."
        },
        mostlyCloses: {
            label: "Mostly closes",
            colour: THEME_COLOURS.blue500,
            sentence: "This gap mostly closes by the medium term."
        },
        reverses: {
            label: "Reverses",
            colour: THEME_COLOURS.blue700,
            dash: "dash",
            sentence: "This gap reverses by the medium term."
        },
        smallThroughout: {
            label: "Small throughout",
            colour: THEME_COLOURS.grey500,
            sentence: "This comparison is small throughout."
        }
    },
    signDirections: {
        comparisonMinusReference: "comparison_group_pct - reference_group_pct",
        referenceMinusComparison: "reference_group_pct - comparison_group_pct"
    }
};

export const CHART_7_TEXT = {
    cardLabels: {
        selector: "Choose a subgroup comparison",
        referenceGroup: "Reference group",
        comparisonGroup: "Comparison group",
        gapChange: "Gap change"
    },
    signCaptions: {
        comparisonMinusReference: "Positive values mean the comparison group has a higher full-time employment rate than the reference group. Negative values mean the gap reverses.",
        referenceMinusComparison: "Positive values mean the reference group has a higher full-time employment rate than the comparison group. Negative values mean the gap reverses."
    }
};
