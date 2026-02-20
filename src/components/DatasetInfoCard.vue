<template>
<div v-if="dataset" style="padding: 20px; background-color: #f4f4f4; border-radius: 10px;">
    <h3>Dataset Info</h3>
    <p><strong>Site:</strong> {{ dataset.site?.sitename ?? 'Unknown' }}</p>
    <p><strong>Dataset Type:</strong> {{ dataset.datasets?.[0]?.datasettype ?? 'N/A' }}</p>
    <p><strong>Contact:</strong> {{ dataset.datasets?.[0]?.datasetpi?.[0]?.contactname ?? 'N/A' }}</p>
    <p><strong>Database:</strong> {{ dataset.database ?? 'N/A' }}</p>
    <p><strong>DOI:</strong> {{ dataset.datasets?.[0]?.doi?.[0] ?? 'N/A' }}</p>
  </div>

</template>


<script setup>
defineProps({ dataset: Object });
</script>