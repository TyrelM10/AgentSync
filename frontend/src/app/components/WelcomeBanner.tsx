import { motion } from 'framer-motion';

const WelcomeBanner = () => {
  return (
    <motion.div
      className="p-4 bg-gray-800/50 backdrop-blur-lg rounded-xl border border-blue-700/30 shadow-lg glow-blue mb-4"
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <h1 className="text-xl font-bold text-blue-400 font-orbitron mb-1">
        Welcome to AgentSync
      </h1>
      <p className="text-sm text-gray-300">
        Your AI-powered productivity hub. Manage emails, Linear issues,
        Notion pages, and Slack messages seamlessly.
      </p>
    </motion.div>
  );
};

export default WelcomeBanner;