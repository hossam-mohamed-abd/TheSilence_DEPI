"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.StatisticsService = void 0;
const statistics_repository_1 = require("./statistics.repository");
class StatisticsService {
    repository = new statistics_repository_1.StatisticsRepository();
    async getStatistics() {
        return this.repository
            .getStatistics();
    }
}
exports.StatisticsService = StatisticsService;
