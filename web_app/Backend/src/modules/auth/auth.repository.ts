import prisma from "../../config/prisma";

class AuthRepository {
  async findByEmail(email: string) {
    return prisma.users.findUnique({
      where: {
        email,
      },
    });
  }

  async create(data: any) {
    return prisma.users.create({
      data,
    });
  }

  async findById(id: bigint) {
    return prisma.users.findUnique({
      where: {
        id,
      },
    });
  }
}

export default new AuthRepository();