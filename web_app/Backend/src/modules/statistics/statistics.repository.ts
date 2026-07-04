import prisma from '../../config/prisma';

export class StatisticsRepository {

  async getStatistics() {

    const [
      medicinesCount,
      pharmaciesCount,
    ] = await Promise.all([

      prisma.drugs.count(),

      prisma.pharmacies.count({
        where: {
          is_active: true,
        },
      }),

    ]);

    return {
      medicinesCount,
      pharmaciesCount,
    };
  }
}