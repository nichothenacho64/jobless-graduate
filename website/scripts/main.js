import { renderChart1, renderChart2, renderChart3 } from "./charts/index.js";
import { CHART_1_ID, CHART_2_ID, CHART_3_ID } from "./config.js";

await renderChart1(CHART_1_ID);
await renderChart2(CHART_2_ID);
await renderChart3(CHART_3_ID);
