"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.StatisticsController = void 0;
const statistics_service_1 = require("./statistics.service");
const service = new statistics_service_1.StatisticsService();
class StatisticsController {
    async getStatistics(req, res) {
        try {
            const data = await service.getStatistics();
            res.json({
                success: true,
                data,
            });
        }
        catch (error) {
            res.status(500).json({
                success: false,
                message: error.message,
            });
        }
    }
}
exports.StatisticsController = StatisticsController;
