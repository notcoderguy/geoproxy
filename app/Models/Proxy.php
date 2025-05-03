<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Proxy extends Model
{
    protected $table = 'proxies';
    protected $fillable = [
        'proxy',
        'ip',
        'port',
        'response_time',
        'protocol',
        'google_pass',
        'anonymity',
        'country',
        'city',
        'isp',
        'status',
        'last_checked'
    ];
    protected $casts = [
        'last_checked' => 'datetime',
    ];
    public function scopeActive($query)
    {
        return $query->where('status', 'active');
    }
    public function scopeInactive($query)
    {
        return $query->where('status', 'inactive');
    }
    public function scopeWithResponseTime($query, $responseTime)
    {
        return $query->where('response_time', '<=', $responseTime);
    }
    public function scopeWithProtocol($query, $protocol)
    {
        return $query->where('protocol', $protocol);
    }
    public function scopeWithAnonymity($query, $anonymity)
    {
        return $query->where('anonymity', $anonymity);
    }
    public function scopeWithCountry($query, $country)
    {
        return $query->where('country', $country);
    }
    public function scopeWithCity($query, $city)
    {
        return $query->where('city', $city);
    }
    public function scopeWithIsp($query, $isp)
    {
        return $query->where('isp', $isp);
    }
    public function scopeWithStatus($query, $status)
    {
        return $query->where('status', $status);
    }
    public function scopeWithLastChecked($query, $lastChecked)
    {
        return $query->where('last_checked', '>=', $lastChecked);
    }
    public function scopeWithIp($query, $ip)
    {
        return $query->where('ip', $ip);
    }
    public function scopeWithPort($query, $port)
    {
        return $query->where('port', $port);
    }
    public function scopeWithGooglePass($query, $googlePass)
    {
        return $query->where('google_pass', $googlePass);
    }
    public function scopeWithUniqueProxy($query, $proxy)
    {
        return $query->where('proxy', $proxy)->distinct();
    }
}
