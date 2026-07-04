import { StatisticsRepository }
from './statistics.repository';

export class StatisticsService {

  private repository =
    new StatisticsRepository();

  async getStatistics() {
    return this.repository
      .getStatistics();
  }
}