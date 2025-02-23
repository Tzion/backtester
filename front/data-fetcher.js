const convertTimestampToUnixTime = (timestampWithTZ) => {
    const date = new Date(timestampWithTZ);
    return Math.floor(date.getTime() / 1000);
};

const fetchCSVData = async (name) => {
    try {
        const filePath = `../data_feeds/${name}.csv`;
        const response = await fetch(filePath);
        const csvText = await response.text();

        return csvText
            .split('\n')
            .slice(1)
            .filter(line => line.trim() !== '')
            .map(line => {
                const [time, open, high, low, close, volume] = line.split(',');
                return {
                    time: convertTimestampToUnixTime(time),
                    open: parseFloat(open),
                    high: parseFloat(high),
                    low: parseFloat(low),
                    close: parseFloat(close),
                    volume: parseFloat(volume)
                };
            });
    } catch (error) {
        console.error('Error reading CSV file:', error);
        return [];
    }
};

export const fetchOHLCV = async (name) => {
    const dataFetcher = fetchCSVData; // later we'll use database dataFetcher
    return dataFetcher(name);
};