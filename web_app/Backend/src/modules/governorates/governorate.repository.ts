import prisma from '../../config/prisma';

class GovernorateRepository {
  async getByCountry(countryId: number) {
    return prisma.governorates.findMany({
      where: {
        country_id: BigInt(countryId),
      },
      orderBy: {
        name: 'asc',
      },
    });
  }

  async create(
    name: string,
    countryId: number
  ) {
    return prisma.governorates.create({
      data: {
        name,
        countries: {
          connect: {
            id: BigInt(countryId),
          },
        },
      },
    });
  }
}

export default new GovernorateRepository();