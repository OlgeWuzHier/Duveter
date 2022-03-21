export default function getTilesBackgrounds() {
  const names = [
    'starter',
    'straightSmall',
    'straightMedium',
    'straightBig',
    'elongatedCross',
    'skewedCross',
    'regularCross',
    'smallCross',
    'zee',
    'smallZee1',
    'smallZee2',
    'skewedZee',
    'regularCrossHhalf',
    'smallCrossHalf',
    'bigTee',
    'smallTee',
    'elBig',
    'elMedium1',
    'elMedium2',
    'elSmall1',
    'elSmall2',
    'square',
    'squareAppendix',
    'squareAppendixLong',
    'squareAppendixCurved',
    'rectangleAppendixes',
    'hat',
    'zeeFat',
    'ceeSmall',
    'ceeBig',
    'hehe',
    'tetris',
    'spaceBattleship',
    'special4',
    'special3',
    'special2',
    'special1',
    'special0',
  ];

  const backgrounds = Array.from({ length: 42 }, (_, i) => i + 1);

  for (let i = backgrounds.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [backgrounds[i], backgrounds[j]] = [backgrounds[j], backgrounds[i]];
  }

  return Object.fromEntries(names.map((name, index) => [name, backgrounds[index]]));
}
