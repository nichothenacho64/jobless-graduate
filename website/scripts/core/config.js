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
    chart1a: "Australians with degrees have increased since 2016",
    chart1b: "Younger workers are concentrated in lower-skill work",
    chart2: "Full-time employment is weakest 4–6 months after graduation",
    chart3: "Early graduate employment gaps are not evenly shared",
    chart4: "Some early gaps narrow, but others remain",
    chart5: "Some fields improve strongly after the first graduate year",
    chart6: "Full-time employment gains do not always mean better work fit",
};

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
    background: "#FFFDF9",
    label: "#e5e0d7"
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

export const GLOBAL_LAYOUT = {
    paper_bgcolor: TRANSPARENT_BACKGROUND,
    plot_bgcolor: TRANSPARENT_BACKGROUND
};

export const GLOBAL_CONFIG = {
    responsive: true,
    displayModeBar: false
};

export const GLOBAL_TRACES = {
    hoverlabel: {
        align: "left",
        font: { size: 12 }
    },
    marker: { line: { width: 1.5 } }
};

export const VIEWPORT_MEDIA_QUERIES = {
    large: "(min-width: 992px)"
};


// shared chart labels
export const SOURCE_LABEL_TEXT = {
    singular: "Source",
    plural: "Sources"
};

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

export const DISCIPLINE_FAMILY_RENDERING = {
    order: [
        "strongest",
        "stronger",
        "weaker",
        "weakest"
    ],
    colours: {
        strongest: THEME_COLOURS.blue700,
        stronger: THEME_COLOURS.blue500,
        weaker: THEME_COLOURS.amber500,
        weakest: THEME_COLOURS.amber700
    }
};

export const DUMBBELL_LINE = {
    default: {
        width: 2.5,
        color: THEME_COLOURS.grey500
    },
    emphasised: {
        width: 2.5,
        color: THEME_COLOURS.amber700
    }
};

export const DIAGONAL_LINE = {
    color: THEME_COLOURS.text,
    width: 2,
    dash: "dash"
};

export const ANNOTATION_FONT = {
    default: {
        family: FONT_FAMILY,
        size: 12,
        color: THEME_COLOURS.text
    }
};

export const LINE_ANNOTATIONS = {
    backgroundOpacity: 0.9,
    diagonalTextAngle: -12,
    offset: 8
};

export const CHART_RANGES = {
    chart1a: { x: [2016, 2025.1], y: [4500000, 7000000] },
    chart1b: { x: null, y: [0, 112] },
    chart2: { x: null, y: [59, 96] },
    chart3: { x: [55, 86], y: null },
    chart4: { x: [-3, 19], y: null },
    chart5: { x: [45, 100], y: [45, 100] },
    chart6: { x: [0, 38.2], y: [-8, 17] }, // x upper bound medianEmploymentGain * 2
    chart7: { x: null, y: [-5, 17.4] }
};


// chart 1a
export const CHART_1A_DIMENSIONS = {
    rightMargin: 270
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

export const CHART_3_RENDERING = {
    defaultColour: THEME_COLOURS.amber500,
    homeLanguageDimension: "Home language"
};

export const CHART_3_SHORT_LABELS = {
    "Socio-economic status": "Socio-economic",
    "Disability reported": "Disability",
    "No disability reported": "No disability"
};

export const CHART_4_DIMENSIONS = {
    baseHeight: DUMBBELL_BASE_HEIGHT,
    rowHeight: DUMBBELL_ROW_HEIGHT,
    leftMargin: 280,
    rightMargin: 20,
};


// chart 6
export const CHART_6_RENDERING = {
    leftQuadrantPanelOpacity: 0.05,
    rightQuadrantPanelOpacity: 0.05
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
    }
};

export const CHART_7_VALUES = {
    gapPatternThresholds: {
        nearZero: 1,
        smallThroughout: 2,
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
        selector: "Choose a subgroup comparison:",
        referenceGroup: "Reference group",
        comparisonGroup: "Comparison group",
        gapChange: "Gap change"
    },
    signCaptions: {
        comparisonMinusReference: "Positive values mean the comparison group has a higher full-time employment rate than the reference group. Negative values mean the gap reverses.",
        referenceMinusComparison: "Positive values mean the reference group has a higher full-time employment rate than the comparison group. Negative values mean the gap reverses."
    }
};

// chart annotations
export const ANNOTATION_LABELS = {
    chart1a: [
        {
            year: 2025,
            text: "As of 2025, approximately <br><b>6.8 million</b> Australians <br>hold degrees",
            ax: 40,
            ay: 0
        }
    ],
    chart1b: [
        {
            ageGroup: "15–24",
            text: "15–24 year-olds have the <br><b>largest share</b> of lower skill work",
            ax: 0,
            ay: -40
        }
    ],
    chart4: [
        {
            subgroupDimension: "Home language",
            text: "The home language<br> gap significantly <b>closes</b>",
            ax: 150,
            ay: -26
        },
        {
            subgroupDimension: "Disability",
            text: "The disability gap <b>persists</b>",
            ax: 200,
            ay: -26
        }
    ],
    chart5: [
        {
            studyArea: "Creative arts",
            text: "Creative arts has the largest later recovery",
            xanchor: "left",
            ax: 20,
            ay: -80
        },
        {
            studyArea: "Rehabilitation",
            text: "Rehabilitation is already high after year one",
            xanchor: "left",
            ax: 40,
            ay: -40
        }
    ],
    chart6: [
        {
            studyArea: "Creative arts",
            text: "Creative arts has the<br>biggest work gain,<br>but fit barely improves",
            xanchor: "left",
            ax: 30,
            ay: 55
        },
        {
            studyArea: "Agriculture and environmental studies",
            text: "Agriculture has work and <br>fit improving together",
            xanchor: "left",
            ax: 100,
            ay: -10
        }
    ]
};
