<template>
  <div class="years">
    <div class="btns" style="margin-bottom: 20px;">
      <a-space>
        <a-button type="primary" @click="getToday">今天数据</a-button>
      </a-space>
    </div>

    <a-table
      :columns="columns"
      :data-source="table_list"
      :pagination="false"
      :loading="loading"
    >
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'caozuo'">
          <a-button type="link" @click="goDetail(record)">查看</a-button>
        </template>
      </template>
    </a-table>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, getCurrentInstance } from "vue";
import { useRouter } from 'vue-router';

export default defineComponent({
  setup() {
    const instance: any = getCurrentInstance();
    const columns = [
      { title: "日期", dataIndex: "date", key: "date" },
      { title: "数量", dataIndex: "count", key: "count" },
      { title: "操作", key: "caozuo" },
    ];
    const loading = ref(false);
    const table_list = ref([]);
    const router = useRouter();
    const queryData = () => {
      loading.value = true;
      instance.proxy.$http
        .get("/gateway/api/get_all_date")
        .then((res: any) => {
          const list = res.data.data;
          table_list.value = list;
          loading.value = false;
        })
        .catch(() => {
          loading.value = false;
        });
    };

    const getToday = () => {
      const now = new Date();
      const today = `${now.getFullYear()}-${now.getMonth() + 1}-${now.getDate()}`
      loading.value = true;
      instance.proxy.$http
        .get("/gateway/api/get_years_data", {
          params: {
            date: today
          },
        })
        .then((res: any) => {
          queryData();
          loading.value = false;
        })
        .catch(() => {
          loading.value = false;
        });
    }

    const goDetail = (item) => {
      router.push({
        name: 'yearsDate',
        query: {
          date: item.date
        }
      })
    }

    onMounted(() => {
      queryData();
    });

    return {
      table_list,
      columns,
      loading,
      goDetail,
      getToday
    };
  },
});
</script>

