import { useState } from "react";
import { AppLayout } from "./components/AppLayout/AppLayout";
import { PipelineControls } from "./components/PipelineControls";

function App() {
  const [refreshKey, setRefreshKey] = useState(0);

  const handleRefresh = () => {
    setRefreshKey((k) => k + 1);
  };

  return (
    <AppLayout>
      <PipelineControls key={refreshKey} onRefresh={handleRefresh} />
    </AppLayout>
  );
}

export default App;
