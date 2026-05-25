import { 
    renderChart1, 
    renderChart2, 
    renderChart3, 
    renderChart4, 
    renderChart5, 
    renderChart6a 
} from "./charts/index.js";
import {
    CHART_1_ID,
    CHART_2_ID,
    CHART_3_ID,
    CHART_4_ID,
    CHART_5_ID,
    CHART_6A_ID
} from "./config.js";

await renderChart1(CHART_1_ID);
await renderChart2(CHART_2_ID);
await renderChart3(CHART_3_ID);
await renderChart4(CHART_4_ID);
await renderChart5(CHART_5_ID);
await renderChart6a(CHART_6A_ID);
