import prisma from './config/prisma';

async function test() {
  try {
    const users =
      await prisma.users.findMany();

    console.log(users);
  } catch (err) {
    console.log(err);
  }
}

test();