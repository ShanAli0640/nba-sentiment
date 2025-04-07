export type Player = {
    name: string;
    description: string;
};

export async function getPlayerIDList() {
    // get all player names
    const res = await fetch('http://localhost:8000/players');
    const players = await res.json();
    return players
}
export async function getPlayerDetails(name) {
    const response = await fetch(`http://127.0.0.1:8000/player/${name}`);
    const player = await response.json();
    return player;
}