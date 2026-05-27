import { 
    renderChart1a,
    renderChart1b,
    renderChart2, 
    renderChart3, 
    renderChart4, 
    renderChart5, 
    renderChart6,
    renderChart7,
} from "./charts/index.js";
import {
    CHART_1A_ID,
    CHART_1B_ID,
    CHART_2_ID,
    CHART_3_ID,
    CHART_4_ID,
    CHART_5_ID,
    CHART_6_ID,
    CHART_7_ID,
} from "./config.js";

await renderChart1a(CHART_1A_ID);
await renderChart1b(CHART_1B_ID);
await renderChart2(CHART_2_ID);
await renderChart3(CHART_3_ID);
await renderChart4(CHART_4_ID);
await renderChart5(CHART_5_ID);
await renderChart6(CHART_6_ID);
await renderChart7(CHART_7_ID);
