import { motion } from 'framer-motion';

interface ResponseDisplayProps {
  response: string;
  error: string;
}

const ResponseDisplay = ({ response, error }: ResponseDisplayProps) => {
  return (
    <>
      {response && (
        <motion.div
          className="mt-6 p-6 bg-gradient-to-r from-green-500/20 to-cyan-500/20 backdrop-blur-lg rounded-xl border border-green-500/30"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h2 className="text-lg font-bold text-green-400 mb-2 font-orbitron">Response</h2>
          <p className="text-gray-200">{response}</p>
        </motion.div>
      )}
      {error && (
        <motion.div
          className="mt-6 p-6 bg-gradient-to-r from-red-500/20 to-purple-500/20 backdrop-blur-lg rounded-xl border border-red-500/30"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h2 className="text-lg font-bold text-red-400 mb-2 font-orbitron">Error</h2>
          <p className="text-gray-200">{error}</p>
        </motion.div>
      )}
    </>
  );
};

export default ResponseDisplay;