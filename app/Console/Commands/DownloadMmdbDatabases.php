<?php

namespace App\Console\Commands;

use App\Http\Controllers\MmdbDownloadController;
use Illuminate\Console\Command;

class DownloadMmdbDatabases extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'app:pull:mmdb';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Download mmdb databases from MaxMind.';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        try {
            $controller = new MmdbDownloadController;
            $success = $controller->downloadAll();

            if ($success) {
                $this->info('Successfully downloaded all MMDB databases');

                return 0;
            }

            $this->error('Failed to download MMDB databases');

            return 1;
        } catch (\Exception $e) {
            $this->error('Error downloading MMDB databases: '.$e->getMessage());

            return 1;
        }
    }
}
