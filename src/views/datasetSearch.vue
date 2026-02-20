<script setup>
import DatasetInfoCard from '@/components/DatasetInfoCard.vue';
 import { ref, onMounted, computed, watch, nextTick } from 'vue';
 import CascadeSelect from 'primevue/cascadeselect';
 import ProgressSpinner from 'primevue/progressspinner';
 import Button from 'primevue/button';
 import 'primeicons/primeicons.css';
 import Badge from 'primevue/badge';
//  import '@primevue/themes/lara-light-indigo/theme.css'; // Theme
//  import 'primevue/resources/primevue.min.css'; // Core styles
 import 'primeicons/primeicons.css'; // Icons
 import InputText from 'primevue/inputtext';
import TabPanel from 'primevue/tabpanel';
import TabView from 'primevue/tabview';
import Panel from 'primevue/panel';
const myMap = ref(null);
const sitelinks = ref([]);
const sitelinktypes = ref([]);
const sitenames = ref([]);
const collectionunitnames = ref([]);
const result = ref([]);
const sitelinks_pi = ref([]);
const sitelinktypes_pi = ref([]);
const sitenames_pi = ref([]);
const siteids_pi = ref([]);
const collectionunitnames_pi = ref([]);
const contactnames_pi = ref([]);
const result_pi = ref([]);
// Dataset ID
const attemptedDataSearch = ref(false);
const datasetIdInput = ref('');
const selectedDataset = ref(null);
const processingId = ref(false);

const searchByDatasetId = async () => {
    attemptedDataSearch.value = true;
  const id = datasetIdInput.value.trim();
  if (!id) return;

  try {
    processingId.value = true;
    const response = await fetch(`https://api.neotomadb.org/v2.0/data/datasets/${id}`);
    const json = await response.json();
    selectedDataset.value = json.data?.[0] ?? null;
    // console.log("Fetched Dataset:", selectedDataset.value);
    console.log("Fetched Dataset (raw):", JSON.parse(JSON.stringify(selectedDataset.value)));
  } catch (err) {
    console.error("Failed to fetch dataset:", err);
    selectedDataset.value = null;
  } finally {
    processingId.value = false;
  }
};
//const route = useRoute();
 const neotomaapi = import.meta.env.VITE_APP_API_ENDPOINT ?? 'https://api.neotomadb.org'
 const siteNameinput = ref('');
 const PI_nameinput_last = ref('');
 const datasets = ref([]);
  const datasets_pi = ref([]);
 const outputDatasets = ref([]);
 var ids = ref([]);
 const ready = ref(false);
  const ready2 = ref(false);
const processing = ref(false);
const processing2 = ref(false);
 async function findSite(siteName) {
  try {
    siteName = siteName.replace(/[^a-zA-Z0-9]/g, "%");
    console.log(siteName);
    ready.value = false;
    processing.value = true;
    const res1 = await fetch(neotomaapi + "/v2.0/data/sites?sitename=%" + siteName + '%&limit=50', {
      method: "GET",
      headers: { 'content-type': 'application/json' }
    });
    const json1 = await res1.json();
    const sites = json1.data ?? {};
    console.log(sites);
    
    datasets.value = [...sites];
    console.log(datasets.value);
    nextTick(() => {
      console.log("After update:", datasets.value[0].sitename); // This will log the updated value
    });
    sitelinks.value = [];
    sitelinktypes.value = [];
    sitenames.value = [];
    collectionunitnames.value = [];
    datasets.value.forEach(site => {
        site.collectionunits.forEach(coll => {
                sitenames.value.push(site.sitename);
                sitelinks.value.push(("https://data.neotomadb.org/datasets/" + coll.datasets[0].datasetid))
                sitelinktypes.value.push(coll.datasets[0].datasettype)
                if (coll.collectionunit !== null) {
                collectionunitnames.value.push(coll.collectionunit) } else {
                    collectionunitnames.value.push('Unnamed collection unit')
                }
            
        })
    }) 
    console.log(encodeURIComponent("Devil's Lake"))
    const siteData = {};
Object.keys(sitenames.value).forEach(index => {
    const name = sitenames.value[index];
    const link = sitelinks.value[index];
    const type = sitelinktypes.value[index];
    const collunit = collectionunitnames.value[index];
    if (!siteData[name]) {
        siteData[name] = { sitename: name, collunits: [] };
    }
    let collunitEntry = siteData[name].collunits.find(cu => cu.name === collunit);
    if (!collunitEntry) {
    // If it doesn't exist, create a new entry for this collunit
        collunitEntry = { name: collunit, datasets: [] };
        siteData[name].collunits.push(collunitEntry);
}
// Add dataset to the collunit's dataset array
    collunitEntry.datasets.push({ link, type });
});
// Convert to an array
result.value = Object.values(siteData);
console.log(result.value);
result.value.sort((a, b) => a.sitename.localeCompare(b.sitename));
ready.value =true;
processing.value = false;
  } catch (err) {
    console.log(err);
    return {};
  }
}
function gotosite(link) {
    window.open(link,'_blank');
}
async function find_byPI(PIname_last) {
  try {
   // PIname_last = PIname_last.replace(/[^a-zA-Z0-9]/g, "%");
    console.log(PIname_last);
    ready2.value = false;
    processing2.value = true;
   // const encodedName = encodeURIComponent('%' + PIname_last + '%'); Changed from familyname= to contactname=
//     const res2 = await fetch(
//   neotomaapi + "/v2.0/apps/datasetpi?contactname=" + encodeURIComponent(PIname_last),
//   {
//     method: "GET",
//     headers: { 'content-type': 'application/json' }
//   }
// );
const res2 = await fetch(neotomaapi + "/v2.0/apps/datasetpi?contactname=" + PIname_last, {
  method: "GET",
  headers: { 'content-type': 'application/json' }
});
    //console.log(PIName);
    const json2 = await res2.json();
    const rawData = json2.data ?? [];
console.log("Raw Data:", rawData);

// Normalize search input
const input = PIname_last.trim().toLowerCase().replace(/[.,]/g, '').split(/\s+/);

// Filter based on contactname, firstname, or familyname
const filtered = rawData.filter(entry => {
  const combined = (
    (entry.contactname?.toLowerCase() || '') +
    (entry.firstname?.toLowerCase() || '') +
    (entry.familyname?.toLowerCase() || '')).replace(/[.,]/g, ''); // Remove punctuation
  // Split combined string into words and check if all input words are included
  return input.every(word => combined.includes(word));
});

// Use filtered data
datasets_pi.value = [...filtered];
console.log(datasets_pi.value);
    console.log(datasets_pi.value);
    nextTick(() => {
    if (datasets_pi.value.length > 0) {
      console.log("After update:", datasets_pi.value[0].sitename);
    } else {
      console.log("No matching results — nothing to log.");
    }
  });
    contactnames_pi.value=[];
    sitelinks_pi.value = [];
    sitelinktypes_pi.value = [];
    sitenames_pi.value = [];
    siteids_pi.value = [];
    collectionunitnames_pi.value = [];
    if (datasets_pi.value.length > 0) {
      datasets_pi.value.forEach(site => {
        if (site && site.sitename && site.datasetid && site.contactname && site.datasettype && site.siteid) {
          // Ensure site.sitename and site.datasetid are defined before pushing
          contactnames_pi.value.push(site.contactname);
          sitenames_pi.value.push(site.sitename);
          siteids_pi.value.push(site.siteid);
          sitelinks_pi.value.push("https://data.neotomadb.org/datasets/" + site.datasetid);
          sitelinktypes_pi.value.push(site.datasettype);

          if (site.collunitname != null) {
            collectionunitnames_pi.value.push(site.collunitname);
          } else {
            collectionunitnames_pi.value.push("Unnamed collection unit");
  }
}
  });
} else {
  console.log("No data to populate site values.");
}
    const siteData_pi = {};
Object.keys(contactnames_pi.value).forEach(index => {
    const contactname_pi = contactnames_pi.value[index];
    const sitename_pi = sitenames_pi.value[index];
    const siteid_pi = siteids_pi.value[index];
    const link_pi = sitelinks_pi.value[index];
    const type_pi = sitelinktypes_pi.value[index];
    const collunit_pi = collectionunitnames_pi.value[index];
    if (!siteData_pi[contactname_pi]) {
        siteData_pi[contactname_pi] = { contactname: contactname_pi, sites: [] };
    }
    let siteEntry = siteData_pi[contactname_pi].sites.find(si => si.siteid === siteid_pi);
    if (!siteEntry) {
    // If it doesn't exist, create a new entry for this collunit
        siteEntry = { sitename: sitename_pi, siteid: siteid_pi, collunits: [] };
        siteData_pi[contactname_pi].sites.push(siteEntry);
}
let collunitEntry = siteEntry.collunits.find(cu => cu.name === collunit_pi);
    if (!collunitEntry) {
    // If it doesn't exist, create a new entry for this collunit
        collunitEntry = { name: collunit_pi, datasets: [] };
        siteEntry.collunits.push(collunitEntry);
}
// Add dataset to the collunit's dataset array
    collunitEntry.datasets.push({ link_pi, type_pi });
});
// Convert to an array
result_pi.value = Object.values(siteData_pi);
console.log(result_pi.value);
result_pi.value.sort((a, b) => a.contactname.localeCompare(b.contactname));
ready2.value =true;
processing2.value = false;
  } catch (err) {
    console.log(err);
    return {};
  }
}
</script>
<style>
  .map {
    width: 100%;
    height: 400px; /* Adjust the height as needed */
  }
div {
    background-color: #f4f4f2;
}
* {
   font-family: "Nunito Sans", sans-serif; 
   color: #47535b;
   font-size:16px;
}
a {
    color: #1D5183;
    font-weight: 900;
}
.p-tabview-tablist-item {
  background-color: #f4f4f2;
  color: #47535b;
  font-weight: normal;
  border: 1px solid transparent;
}

.p-tabview-tablist-item-active {
  background-color: #b6b3ab !important;
  color: #000 !important;
  font-weight: bold !important;
  border: 1px solid #778A97 !important;
  border-bottom: none !important;
}

.p-tabview-tablist-item-active .p-tabview-nav-link {
  color: #000 !important;
}

.p-tabview-nav-link:hover {
  background-color: #d3d3d3;
  color: #000;
  cursor: pointer;
}
li.p-tabview-header.p-highlight {
    border-color: #778A97;
}
.btn2 {
    font-weight: 900;
}
.btn2:focus-visible {
    box-shadow: 0 0 0 0.2rem rgb(119, 138, 151);
}
.btn_link {
    color: #1D5183;
    border-color: #1D5183;
}
div.p-panel-header {
    background-color: #d3d1cc;
    border-color: #d3d1cc;
    padding-left: 5px;
}
div.p-panel-icons {
    background-color: #d3d1cc;
    border-color: #d3d1cc;
}
.p-panel-title {
    font-size:20px;
}
.p-panel-content {
    background-color:#d3d1cc;
    border-color: #d3d1cc;
}
.p-tabview-panels {
    padding-left:0px;
}
.p-inputtext:enabled:focus {
    border-color:#1D5183;
    box-shadow: 0 0 0 0.2rem #1D5183;
}
.p-inputtext:enabled:hover {
    border-color:#1D5183;
}
body {
    display:block;
    padding-top: 40px;
}
.p-inputtext {
    background-color: #f0f0f0 !important;
    border: 1px solid #778A97 !important;
    color: #000 !important;
    padding: 0.5rem !important;
    border-radius: 4px !important;
}
</style>
<template>
    <div style="width:1000px; margin: 0 auto; max-width: 95%;">
        <div>
            <div>
                    <TabView>
                        <TabPanel header="Site Search">
                            <div style="display:grid;grid-template-columns:1fr 1fr;margin-bottom:2%;">
                                <InputText id ="site-name-input" name ="site-name-input" type="text" v-model="siteNameinput" placeholder ="Enter Site Name" />
                                <div style="margin-left:2%;">
                                    <Button style="background-color:#b6b3ab;border-color:#778A97;" @click='findSite(siteNameinput)' class="btn2">Submit</Button>
                                </div>
                            </div>
                             <div v-if="!ready && !processing">
    </div>
    <div v-if="!ready && processing">
        <ProgressSpinner />
    </div>
    <div v-else-if='ready && result.length == 0'>
        <p>No site names in Neotoma contain the string you searched for.</p>
    </div>
    <div v-else>
        <div style="display:flex;flex-wrap:wrap;flex-direction:row;align-items:flex-start;">
            <div v-for="(site, index) in result" :key="index"  style="border-radius:20px; background-color: #d3d1cc; padding: 2%;padding-left:2%; margin-bottom: 2%; margin-right:2%;width:225px;border: 1px solid #7c7667;">
                <Panel :header='site.sitename' toggleable :collapsed='true' >
                    <div v-for="coll in site.collunits" style="background-color: #d3d1cc;">
                        <h4>{{coll.name}} </h4>
                        <div v-for="dataset in coll.datasets" style="background-color: #d3d1cc;">
                            <div v-if="dataset.type != null" style="background-color: #d3d1cc; padding-left:5%;padding-right:5%; width:100%;">
                                <div style="justify-self:center;margin-top:5px; border-radius:200px; background-color: #d3d1cc;">
                                    <Button class="btn_link" style="border: 1px solid; border-radius:20px; background-color: #b6b3ab;" @click=gotosite(dataset.link)>{{dataset.type}}</Button>
                                </div>
                            </div>
                        </div>
                    </div> 
                </Panel>
            </div>
        </div>
    </div>
                        </TabPanel>
                        <TabPanel header="PI Search">
                            <div style="display:grid;grid-template-columns:1fr 1fr;margin-bottom:2%;">
                            <InputText type="text" v-model="PI_nameinput_last" placeholder = "Enter PI Name"/>
                            <div style="margin-left:2%;">
                                <Button style="background-color:#b6b3ab;border-color:#778A97;"  @click='find_byPI(PI_nameinput_last)' class="btn2">Submit</Button>
                            </div>
                            </div>
                            <div v-if="!ready2 && !processing2">
    </div>
    <div v-if="!ready2 && processing2">
        <ProgressSpinner />
    </div>
    <div v-else-if='ready2 && result_pi.length == 0'>
        <p>No names in Neotoma contain the string you searched for.</p>
    </div>
    <div v-else>
        <div style="display:flex;flex-wrap:wrap;flex-direction:row;align-items:flex-start;">
            <div v-for="(contact, index) in result_pi" :key="index"  style="border-radius:20px; background-color: #d3d1cc; padding: 2%;padding-left:2%; margin-bottom: 2%; margin-right:2%;width:225px;border: 1px solid #7c7667;">
                <Panel :header='contact.contactname' toggleable :collapsed='true' >
                    <div v-for="site in contact.sites" style="background-color: #d3d1cc;">
                        <Panel :header='site.sitename' toggleable :collapsed='true' style="border: 2px solid #7c7667;">
                             <div v-for="coll in site.collunits" style="background-color: #d3d1cc;">
                        <h4>{{coll.name}} </h4>
                        <div v-for="dataset in coll.datasets" style="background-color: #d3d1cc;">
                            <div v-if="dataset.type_pi != null" style="background-color: #d3d1cc; padding-left:5%;padding-right:5%; width:100%;">
                                <div style="justify-self:center;margin-top:5px; border-radius:200px; background-color: #d3d1cc;">
                                    <Button class="btn_link" style="border: 1px solid; border-radius:20px; background-color: #b6b3ab;" @click=gotosite(dataset.link_pi)>{{dataset.type_pi}}</Button>
                                </div>
                            </div>
                        </div>
                    </div>
                        </Panel>
                    </div> 
                </Panel>
            </div>
        </div>
    </div>
                        </TabPanel>
                        <TabPanel header="Dataset ID Search">
  <div style="display: grid; grid-template-columns: 1fr auto; margin-bottom: 2%;">
    <InputText type="text" v-model="datasetIdInput" placeholder="Enter Dataset ID" />
    <div style="margin-left: 2%;">
      <Button style="background-color:#b6b3ab; border-color:#778A97;" @click="searchByDatasetId" class="btn2">Submit</Button>
    </div>
  </div>

  <div v-if="processingId">
    <ProgressSpinner />
  </div>

  <div v-if="selectedDataset" style="padding: 1rem;">
  <div v-if="selectedDataset" style="display:flex; flex-wrap:wrap; flex-direction:row; align-items:flex-start; margin-top: 1rem;">
  <div style="border-radius:20px; background-color: #d3d1cc; padding: 2%; margin-bottom: 2%; margin-right:2%; width: 225px; border: 1px solid #7c7667;">
    <Panel :header="selectedDataset?.site?.sitename ?? 'Dataset'" toggleable :collapsed="true">
      <div v-if="selectedDataset.site?.datasets?.[0]" style="background-color: #d3d1cc;">
        <p><strong>Type:</strong> {{ selectedDataset.site?.datasets[0].datasettype || 'N/A' }}</p>
        <p><strong>Contact:</strong>
          {{
            (selectedDataset.site?.datasets[0].datasetpi?.[0]?.firstname || '') +
            ' ' +
            (selectedDataset.site?.datasets[0].datasetpi?.[0]?.lastname || '')
          }}
        </p>
        <p><strong>Database:</strong> {{ selectedDataset.site?.datasets[0].database || 'N/A' }}</p>
        <p><strong>DOI:</strong>
          <a :href="`https://doi.org/${selectedDataset.site?.datasets[0].doi}`" target="_blank" style="font-weight: bold; color: #1a237e;">
            {{ selectedDataset.site?.datasets[0].doi }}
          </a>
        </p>
      </div>
    </Panel>
  </div>
</div>
</div>

  <div v-if="attemptedDataSearch && !processingId && selectedDataset === null">
    <p>No dataset found with that ID.</p>
  </div>
</TabPanel>
                    </TabView>
            </div>
   
</div>
</div>
</template>