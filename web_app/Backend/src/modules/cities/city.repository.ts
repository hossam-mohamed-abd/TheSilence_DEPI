import prisma from '../../config/prisma';

class CityRepository {
  async getByGovernorate(
    governorateId: number
  ) {
    return prisma.cities.findMany({
      where: {
        governorate_id:
          BigInt(governorateId),
      },
      orderBy: {
        name: 'asc',
      },
    });
  }

  async create(
    name: string,
    governorateId: number
  ) {
    return prisma.cities.create({
      data: {
        name,
        governorates: {
          connect: {
            id:
              BigInt(governorateId),
          },
        },
      },
    });
  }
}

export default new CityRepository();